import json
from django.core.cache import cache
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.response import Response
from ..serializers import (CreatePatientSerializer, OtpVerifySerializer, ResendCodeSerializers, ResetPasswordRequestSerializer, ResetPasswordConfirmSerializer)
from ..models import PasswordResetToken
from ..random_code_otp import random_otp_code
from ..throttles import PhoneNumberRateThrottle, EmailResetThrottle
from ..services.registration import start_patient_registration, complete_patient_registration
from apps.utils.send_sms_otp import send_otp_register

User = get_user_model()


class CreatePatientAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreatePatientSerializer
    throttle_classes = [PhoneNumberRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        phone_number = user_data['phone_number']
        otp = start_patient_registration(validated_data=user_data)
        return Response({'message': _("کد تایید برای شما ارسال شد"), "otp": f"{otp}"}, status.HTTP_201_CREATED)


class VerifyCodeAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = OtpVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        phone_number = data['phone_number']
        code = data['code']

        data_key = f"otp_registration:{phone_number}"
        cached_data = cache.get(data_key)

        if not cached_data:
            return Response({"message": _("اطلاعات منقضی شده است.")}, status.HTTP_400_BAD_REQUEST)
        
        data = json.loads(cached_data)

        if str(data['otp']) != str(code):
            return Response({"message": _("کد وارد شده صحیح نیست.")}, status.HTTP_400_BAD_REQUEST)
        
        complete_patient_registration(phone_number=phone_number, code=code)

        return Response({"message": _("ثبت‌نام با موفقیت انجام شد.")}, status.HTTP_201_CREATED)


class ResendOtpCodeAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ResendCodeSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        key = f"otp_registration:{phone_number}"
        cache_data = cache.get(key)

        if not cache_data:
            return Response({"message": _("هیچ ثبت‌نام فعالی برای این شماره وجود ندارد.")}, status.HTTP_400_BAD_REQUEST)
        
        data = json.loads(cache_data)
        otp = random_otp_code()
        data['otp'] = otp

        cache.set(key, json.dumps(data), timeout=180)

        send_otp_register.delay(phone_number, otp)

        return Response({"message": _("کد مجدد ارسال شد."), "otp": f"{otp}"}, status.HTTP_201_CREATED)


class PasswordResetAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordRequestSerializer
    throttle_classes = [EmailResetThrottle]


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email'].lower().strip()
        user = User.objects.get(email=email)
        reset_token = PasswordResetToken.objects.create(user=user)

        reset_link = request.build_absolute_uri(reverse_lazy('auth:confirm-reset-password', kwargs={'token':str(reset_token.token)}))

        send_mail(
            subject= _('درخواست تغییر کلمه عبور'),
            message= _(f".برای تغییر کلمه عبور روی لینک زیر کلیک کنید {reset_link}"),
            from_email= 'example@gmail.com',
            recipient_list= [user.email],
            fail_silently= False
        )

        return Response({'detail': 'لینک بازیابی رمز عبور ارسال شد.'}, status=status.HTTP_200_OK)


class ConfirmResetPasswordAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordConfirmSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, 'token': self.kwargs['token']})
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        reset_token = PasswordResetToken.objects.select_related('user').get(token=token)
        user = reset_token.user

        with transaction.atomic():
            user.set_password(new_password)
            user.save(update_fields=['password'])
            reset_token.is_used = True
            reset_token.save(update_fields=['is_used'])

        return Response({'detail': 'رمز عبور با موفقیت تغییر کرد.'}, status=status.HTTP_200_OK)
