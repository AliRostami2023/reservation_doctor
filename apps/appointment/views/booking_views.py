from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Appointment
from ..services.booking import create_patient_appointment
from ..serializers import AppointmentCreateSerializer, PatientAppointmentListSerializer
from ..permissions import IsPatient


class CreateAppointmentView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentCreateSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        create_patient_appointment(
            patient=self.request.user.patient_user,
            doctor=serializer.validated_data['doctor'],
            day=serializer.validated_data['date']['day'],
            time=serializer.validated_data['time'],
        )


class ListAppointmentView(generics.ListAPIView):
    queryset = Appointment.objects.select_related('doctor__user', 'patient__user', 'date')
    serializer_class = PatientAppointmentListSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        return self.queryset.filter(patient__user=self.request.user)
