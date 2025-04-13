from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from .serializers import *
from .models import OtpCode, Doctor, Patient
from .permissions import IsDoctor, IsPatient

User = get_user_model()


class CreatePatientAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreatePatientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': _("کد تایید برای شما ارسال شد")}, status.HTTP_200_OK)
    

class VerifyCodeAPIView(generics.CreateAPIView):
    queryset = OtpCode.objects.select_related("user")
    serializer_class = VerifyCodeSerializer


    def get_serializer_context(self):
        return {'reauest': self.request}

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": _("ثبت نام با موفقیت انجام شد")}, status.HTTP_201_CREATED)
    

class ResendCodeAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResendCodeSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': _('کد تایید مجدد ارسال شد.')}, status.HTTP_200_OK)


class RequestPasswordResetAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordRequestSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('ما یک ایمیل تغییر کلمه عبور برایتان ارسال کردیم')}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class ConfirmResetPasswordViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('کلمه عبور با موفقیت تغییر یافت.')}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CreateDoctorAPIView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = CreateDoctorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': _("ثبت نام با موفقیت انجام شد پس از بررسی به شما اطلاع میدهیم.")}, status.HTTP_201_CREATED)



class ListDoctorProfileAPIView(generics.ListAPIView):
    queryset = Doctor.objects.select_related('user')
    serializer_class = ListProfileDoctorSerializer
    
    
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

