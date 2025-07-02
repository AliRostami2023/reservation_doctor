import requests
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework import serializers
from .models import PasswordResetToken, Doctor, Patient

User = get_user_model()



class CreatePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def validate_phone_number(self, value):
        from django.core.cache import cache

        redis_key = f"otp_registration:{value}"
        if cache.get(redis_key):
            raise serializers.ValidationError(_("یک درخواست ثبت‌نام فعال برای این شماره وجود دارد. لطفاً کد را وارد کنید یا منتظر انقضا بمانید."))
        return value
    
    
class OtpVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        from django.core.cache import cache
        import json

        phone_number = data['phone_number']
        code = data['code']

        redis_key = f"otp_registration:{phone_number}"
        cached_data = cache.get(redis_key)

        if not cached_data:
            raise serializers.ValidationError(_("اطلاعات ثبت‌نامی پیدا نشد یا منقضی شده است."))

        try:
            data_dict = json.loads(cached_data)
        except json.JSONDecodeError:
            raise serializers.ValidationError(_("داده‌های ثبت‌نامی نامعتبر هستند."))

        if str(data_dict.get('otp')) != str(code):
            raise serializers.ValidationError(_("کد وارد شده صحیح نیست."))

        return data


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
        

    # def validate_email(self, value):
    #     email = value.lower().strip()
    #     if not User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError(_('کاربری با این ایمیل وجود ندارد !!!'))
    #     return email


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
        from django.core.cache import cache
        
        redis_key = f"otp_registration:{value}"
        if not cache.get(redis_key):
            raise serializers.ValidationError(_("هیچ ثبت‌نام فعالی برای این شماره وجود ندارد."))
        return value


class CreateDoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', label="نام و نام خانوادگی")
    phone_number = serializers.CharField(source='user.phone_number', label="شماره همراه")
    email = serializers.EmailField(source='user.email', label="ایمیل")
    password = serializers.CharField(source='user.password', label="کلمه عبور")
    captcha_response = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ['full_name', 'email', 'phone_number', 'password', 'Medical_system_code', 'specialty',
                   'captcha_response', 'experience_years']

    def validate_recaptcha(self, captcha_response):
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

