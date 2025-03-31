import random
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.db import transaction, IntegrityError
from django.conf import settings
from datetime import datetime, timedelta
from .models import OtpCode, PasswordResetToken, Doctor, Patient
from .random_code_otp import random_otp_code

User = get_user_model()



class CreatePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        validated_data['user_type'] = 'patient'
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)

            expired_date = datetime.now() + timedelta(minutes=2)
            OtpCode.objects.create(user=user, code=random_otp_code(), expired_date=expired_date)
            print(f"your code is : {random_otp_code()}")
            return user
    

class VerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ['code']
        read_only_fields = ['user', 'expired_date']


    def validate(self, attrs):
        phone_number = self.context['request'].user
        code = attrs.get("code")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("کاربری با این مشخصات وجود ندارد!"))
        
        otp = OtpCode.objects.filter(user=user, code=code).first()

        if not code:
            raise serializers.ValidationError(_("!کد تایید اشتباه است"))
        
        if otp.expired_date_over():
            otp.delete_otp()
            raise serializers.ValidationError(_("کد منقضی شده است!"))
        
        user.is_active = True
        user.save()

        otp.delete()
        return attrs


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('کاربری با این ایمیل یافت نشد'))
        return value
        

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        reset_token = PasswordResetToken.objects.create(user=user)

        reset_link = f"{self.context['request'].build_absolute_uri(reverse_lazy('reset-password', kwargs={'token':str(reset_token.token)}))}"
        
        send_mail(
            subject= "درخواست تغییر کلمه عبور",
            message= f"برای تغییر کلمه عبور بر روی این لینک کلیک کنید {reset_link}",
            from_email= settings.EMAIL_HOST_USER,
            recipient_list= [user.email],
            fail_silently= False
        )

        return reset_token


class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        password1 = attrs['new_password']
        password2 = attrs['confirm_password']

        if password1 and password1 != password2:
            raise serializers.ValidationError(_('لطفا کلمه عبور یکسان وارد کنید!'))
        elif len(password1) < 8:
            raise serializers.ValidationError(_('کلمه عبور باید شامل 8 کاراکتر یا عدد باشد !!!'))
        return password1

    def validate_token(self, value):
        try:
            reset_token = PasswordResetToken.objects.get(is_used=False, token=value)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError(_('لینک نامعتبر است!'))

        if not reset_token.is_valid():
            raise serializers.ValidationError(_('لینک مقضی شده است!'))
        return value
    
    def save(self, **kwargs):
        reset_token = PasswordResetToken.objects.get(token=self.validated_data['token'])
        user = reset_token.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        reset_token.is_used = True
        reset_token.save()

class ResendCodeSerializers(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=11)


    def validate_phone_number(self, value):
        try:
            User.objects.get(phone_number=value)
        except User.DoesNotExist:
            raise  serializers.ValidationError(_("شماره تلفن وجود ندارد !"))
        return value


    def create(self, validated_data):
        user = User.objects.get(phone_number=validated_data['phone_number'])

        otp_code = random_otp_code()
        expire_date = datetime.now() + timedelta(minutes=2)

        OtpCode.objects.update_or_create(user=user, defaults={'code': otp_code, 'expired_date': expire_date})

        print(f"Resend code for {user.phone_number} : {otp_code}")
        return user


class CreateDoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    phone_number = serializers.CharField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Doctor
        fields = ['full_name', 'email', 'phone_number', 'Medical_system_code', 'specialty', 'experience_years']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        with transaction.atomic():
            user, created = User.objects.get_or_create(is_active=False, email=user_data['email'], defaults=user_data)

            if created or user.user_type != 'doctor':
                user.user_type = 'doctor'
                random_pass = random.randint(10000000, 99999999)
                user.password = (str(random_pass))
                user.save()

            if Doctor.objects.filter(user=user).exists():
                raise serializers.ValidationError(_("این پزشک قبلاً ثبت شده است."))

            try:
                doctor = Doctor.objects.create(user=user, **validated_data)
                return doctor
            except IntegrityError:
                raise serializers.ValidationError(_("مشکلی در ثبت پزشک رخ داده است. لطفاً دوباره تلاش کنید."))
            

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email', 'last_login']


class ProfilePatientSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


class ProfileDoctorSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'
        

class UpdateProfilePatientSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    brithday = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Patient
        fields = ['id', 'user', 'avatar', 'national_code', 'brithday', 'gender', 'about_me', 'address']


class UpdateProfileDoctorSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    brithday = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Doctor
        fields = ['id' ,'avatar', 'national_code', 'brithday', 'about_me', 'address', 'Medical_system_code', 'specialty', 'experience_years']

