from django.http import Http404
from rest_framework import permissions, generics
from ..models import Patient
from ..permissions import IsPatient
from ..selectors.profiles import patient_profiles
from ..serializers import (ListProfilePatientSerializer, RetriveProfilePatientSerializer,
    UpdateProfilePatientSerializer)


class ListPatientProfileAPIView(generics.ListAPIView):
    queryset = patient_profiles()
    serializer_class = RetriveProfilePatientSerializer
    permission_classes = [permissions.IsAdminUser]


class RetrivePatientProfileAPIView(generics.RetrieveAPIView):
    queryset = patient_profiles()
    serializer_class = RetriveProfilePatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_object(self):
        try:
            return self.queryset.get(user=self.request.user)
        except Patient.DoesNotExist:
            raise Http404("پروفایل بیماری برای این کاربر یافت نشد.")


class UpdatePatientProfileAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = patient_profiles()
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
