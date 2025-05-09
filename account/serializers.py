import requests
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework import serializers
from .models import OtpCode, PasswordResetToken, Doctor, Patient

User = get_user_model()



class CreatePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    

class OtpVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=5)

    def validate(self, data):
        try:
            user = User.objects.get(phone_number=data['phone_number'])
            try:
                otp = OtpCode.objects.get(user=user)
                if otp.expired_date_over():
                    otp.delete_otp()
                    raise serializers.ValidationError(_('کد تایید منقضی شده است'))
                if otp.code != data['code']:
                    raise serializers.ValidationError(_('کد تایید نادرست است'))
            except OtpCode.DoesNotExist:
                raise serializers.ValidationError(_('کد تایید یافت نشد'))
        except User.DoesNotExist:
            raise serializers.ValidationError(_('کاربری با این شماره تلفن یافت نشد'))
        
        return data
    


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
        

    def validate_email(self, value):
        email = value.lower().strip()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('کاربری با این ایمیل وجود ندارد !!!'))
        return email


class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        password1 = attrs['new_password']
        password2 = attrs['confirm_password']

        if password1 and password1 != password2:
            raise serializers.ValidationError(_('لطفا کلمه عبور یکسان وارد کنید!'))
        elif len(password1) < 8:
            raise serializers.ValidationError(_('کلمه عبور باید شامل 8 کاراکتر یا عدد باشد !!!'))
        
        return attrs


    def validate_token(self, value):
        try:
            reset_token = PasswordResetToken.objects.get(is_used=False, token=value)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError(_('لینک نامعتبر است!'))

        if not reset_token.is_valid():
            raise serializers.ValidationError(_('لینک مقضی شده است!'))
        return value


class ResendCodeSerializers(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=11)


    def validate_phone_number(self, value):
        try:
            User.objects.get(phone_number=value)
        except User.DoesNotExist:
            raise  serializers.ValidationError(_("شماره تلفن وجود ندارد !"))
        return value


class CreateDoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    phone_number = serializers.CharField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')
    captcha_response = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ['full_name', 'email', 'phone_number', 'Medical_system_code', 'specialty',
                  'captcha_response', 'experience_years']

    def validate_recaptcha(self, captcha_response):
        """اعتبارسنجی reCAPTCHA با سرور گوگل"""

        secret_key = settings.RECAPTCHA_PRIVATE_KEY
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': secret_key,
                'response': captcha_response
            }
        )
        result = response.json()
        if not result.get('success'):
            raise serializers.ValidationError(_('reCAPTCHA verification failed.'))
        return True
    

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email', 'last_login']


class ListProfilePatientSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


class RetriveProfilePatientSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


class UpdateProfilePatientSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    brithday = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Patient
        fields = ['id', 'user', 'avatar', 'national_code', 'brithday', 'gender', 'about_me', 'address']


class ListProfileDoctorSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'


class RetriveProfileDoctorSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'


class UpdateProfileDoctorSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    brithday = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'avatar', 'national_code', 'brithday', 'about_me', 'address',
                   'Medical_system_code', 'specialty', 'experience_years']

