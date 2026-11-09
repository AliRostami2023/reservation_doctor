from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from ..filters import DoctorFilter
from ..models import Doctor
from ..permissions import IsDoctor
from ..selectors.profiles import doctor_profiles
from ..serializers import (CreateDoctorSerializer, ListProfileDoctorSerializer,
    RetriveProfileDoctorSerializer, UpdateProfileDoctorSerializer)

User = get_user_model()


class CreateDoctorAPIView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = CreateDoctorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data.pop('captcha_response')

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
                user.set_password(user_data['password'])
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
    queryset = doctor_profiles()
    serializer_class = ListProfileDoctorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = DoctorFilter
    search_fields = ['full_name', 'specialty']


class RetriveDoctorProfileAPIView(generics.RetrieveAPIView):
    queryset = doctor_profiles()
    serializer_class = RetriveProfileDoctorSerializer


class UpdateDoctorProfileAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = doctor_profiles()
    serializer_class = UpdateProfileDoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    
    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        else:
            return super().get_permissions()
