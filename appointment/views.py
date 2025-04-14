from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import AvailableTime, Appointment
from .serializers import *
from .permisions import IsDoctor, IsPatient



class CreateAvailableTimeView(generics.CreateAPIView):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeCreateSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor_profile)


class ListAvailableTimeView(generics.ListAPIView):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeListSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return self.queryset.filter(doctor=self.request.user.doctor_profile)


class UpdateDeleteAvailableTimeView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeUpdateSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return self.queryset.filter(doctor=self.request.user.doctor_profile)


class CreateAppointmentView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentCreateSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient_user)


class ListAppointmentView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentListSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        return self.queryset.filter(patient=self.request.user.patient_user)
    

class PublicAvailableTimesForDoctorView(generics.ListAPIView):
    serializer_class = AppointmentListSerializer

    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor')
        date = self.request.query_params.get('date')

        queryset = AvailableTime.objects.filter(is_active=True)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if date:
            queryset = queryset.filter(date__day=date)

        return queryset
    