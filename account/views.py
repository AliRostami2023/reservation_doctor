from rest_framework import viewsets, status, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .serializers import CreatePatientSerializer, VerifyCodeSerializer, ResendCodeSerializers, \
                    ResetPasswordConfirmSerializer, ResetPasswordRequestSerializer, CreateDoctorSerializer
from .models import OtpCode, Doctor


User = get_user_model()


class CreatePatientViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreatePatientSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': _("کد تایید برای شما ارسال شد")}, status.HTTP_200_OK)
    

class VerifyCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = OtpCode.objects.select_related("user")
    serializer_class = VerifyCodeSerializer


    def get_serializer_context(self):
        return {'reauest': self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": _("ثبت نام با موفقیت انجام شد")}, status.HTTP_201_CREATED)
    

class ResendCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ResendCodeSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': _('کد تایید مجدد ارسال شد.')}, status.HTTP_200_OK)


class RequestPasswordResetViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ResetPasswordRequestSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('ما یک ایمیل تغییر کلمه عبور برایتان ارسال کردیم')}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class ConfirmResetPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ResetPasswordConfirmSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('کلمه عبور با موفقیت تغییر یافت.')}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CreateDoctorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Doctor.objects.all()
    serializer_class = CreateDoctorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': _("ثبت نام با موفقیت انجام شد پس از بررسی به شما اطلاع میدهیم.")}, status.HTTP_201_CREATED)
