import random
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.http import Http404
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import DoctorFilter
from datetime import datetime, timedelta
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from .serializers import *
from .models import OtpCode, Doctor, Patient
from .permissions import IsDoctor, IsPatient
from .random_code_otp import random_otp_code
from .throttles import PhoneNumberRateThrottle, EmailResetThrottle

User = get_user_model()


class CreatePatientAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreatePatientSerializer
    throttle_classes = [PhoneNumberRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        user_data['user_type'] = 'patient'

        with transaction.atomic():
            user = User.objects.create_user(**user_data)

            expired_date = datetime.now() + timedelta(minutes=5)
            otp_code = random_otp_code()
            OtpCode.objects.create(user=user, code=otp_code, expired_date=expired_date)
            print(f"your code is : {otp_code}")

            return Response({'message': _("کد تایید برای شما ارسال شد")}, status.HTTP_201_CREATED)
    

class VerifyCodeAPIView(generics.CreateAPIView):
    queryset = OtpCode.objects.select_related("user")
    serializer_class = OtpVerifySerializer

    def post(self, request):
        with transaction.atomic():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']

            try:    
                user = User.objects.get(phone_number=phone_number)
                otp = OtpCode.objects.get(user=user, code=code)
    
                user.is_active = True
                user.save()
                otp.delete()
                return Response({"message": _("ثبت نام با موفقیت انجام شد.")}, status.HTTP_201_CREATED)
            except (User.DoesNotExist, OtpCode.DoesNotExist):
                return Response({"message": _("کاربر یافت نشد")})
    


class ResendOtpCodeAPIView(generics.GenericAPIView):
    queryset = OtpCode.objects.select_related("user")
    serializer_class = ResendCodeSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        user = User.objects.get(phone_number=phone_number)
        code = random_otp_code()
        OtpCode.objects.update_or_create(
            user=user,
            defaults={
                "code": code,
                "create_at": timezone.now(),
                "expired_date": timezone.now() + timedelta(minutes=5)
            }
        )

        print(f"code for {phone_number} is = {code}")

        return Response({"message": _("کد مجدد ارسال شد")})



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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.kwargs['token']
        new_password = serializer.validated_data['new_password']

        reset_token = PasswordResetToken.objects.get(token=token)
        user = reset_token.user

        user.set_password(new_password)
        user.save()

        reset_token.is_used = True
        reset_token.save()

        return Response({'detail': 'رمز عبور با موفقیت تغییر کرد.'}, status=status.HTTP_200_OK)


class CreateDoctorAPIView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = CreateDoctorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        captcha_response = serializer.validated_data.pop('captcha_response')
        self.validate_recaptcha(captcha_response)

        user_data = serializer.validated_data.pop('user')
        validated_data = serializer.validated_data

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                is_active=False,
                email=user_data['email'],
                defaults=user_data
            )

            if created or user.user_type != 'doctor':
                user.user_type = 'doctor'
                random_pass = random.randint(10000000, 99999999)
                user.password(str(random_pass)) 
                user.save()

            if Doctor.objects.filter(user=user).exists():
                return Response(
                    {'error': _('این پزشک قبلاً ثبت شده است.')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                Doctor.objects.create(user=user, **validated_data)
                return Response(
                    {'message': _('ثبت نام با موفقیت انجام شد پس از بررسی به شما اطلاع میدهیم.')},
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    {'error': _('مشکلی در ثبت پزشک رخ داده است. لطفاً دوباره تلاش کنید.')},
                    status=status.HTTP_400_BAD_REQUEST
                )


class ListDoctorProfileAPIView(generics.ListAPIView):
    queryset = Doctor.objects.select_related('user')
    serializer_class = ListProfileDoctorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = DoctorFilter
    search_fields = ['full_name', 'specialty']
    
    
class RetriveDoctorProfileAPIView(generics.RetrieveAPIView):
    queryset = Doctor.objects.select_related('user')
    serializer_class = RetriveProfileDoctorSerializer
    
    
class UpdateDoctorProfileAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Doctor.objects.select_related('user')
    serializer_class = UpdateProfileDoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    
    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        else:
            return super().get_permissions()
    


class ListPatientProfileAPIView(generics.ListAPIView):
    queryset = Patient.objects.select_related('user')
    serializer_class = RetriveProfilePatientSerializer
        

class RetrivePatientProfileAPIView(generics.RetrieveAPIView):
    queryset = Patient.objects.select_related('user')
    serializer_class = RetriveProfilePatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_object(self):
        try:
            return self.queryset.get(user=self.request.user)
        except Patient.DoesNotExist:
            raise Http404("پروفایل بیماری برای این کاربر یافت نشد.")
    
    
class UpdatePatientProfileAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Patient.objects.select_related('user')
    serializer_class = UpdateProfilePatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_object(self):
        try:
            return self.queryset.get(user=self.request.user)
        except Patient.DoesNotExist:
            raise Http404("پروفایل بیماری برای این کاربر یافت نشد.")
    
    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        else:
            return super().get_permissions()

