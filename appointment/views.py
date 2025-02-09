from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import AvailableTime, Appointment
from .serializers import AvailableTimSerializer, AppointmentSerializer
from .permisions import IsDoctor, IsPatient



class AvailableTimeViewSet(ModelViewSet):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    # def get_queryset(self):
    #     if hasattr(self.request.user, 'doctor_profile'):
    #         return self.queryset.filter(doctor=self.request.user.doctor_profile)
    #     return AvailableTime.objects.none()

    # def get_queryset(self):
    #     return self.queryset.filter(doctor=self.request.user.doctor_profile)

    def get_queryset(self):
        doctor_profile = getattr(self.request.user, 'doctor_profile', None)
        if doctor_profile:
            return self.queryset.filter(doctor=doctor_profile.id)
        return self.queryset.none()



class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        if hasattr(self.request.user, 'patient_user'):
            return self.queryset.filter(patient=self.request.user.patient_user)
        return self.queryset.none()
