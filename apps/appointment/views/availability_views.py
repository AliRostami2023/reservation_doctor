from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from ..models import AvailableTime, AppointmentDay
from ..serializers import (AvailableTimeCreateSerializer, AvailableTimeListSerializer,
    AvailableTimeUpdateSerializer, AppointmentListSerializer)
from ..permissions import IsDoctor
from ..selectors.availability import public_doctor_availability


class CreateAvailableTimeView(generics.CreateAPIView):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeCreateSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        date_data = serializer.validated_data.pop("date")
        day = date_data.get("day")

        appointment_day, _ = AppointmentDay.objects.get_or_create(day=day)

        serializer.save(
            doctor=self.request.user.doctor_profile,
            date=appointment_day
        )


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


class PublicAvailableTimesForDoctorView(generics.ListAPIView):
    serializer_class = AppointmentListSerializer

    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor')
        date = self.request.query_params.get('date')

        if not doctor_id:
            raise serializers.ValidationError({'doctor': 'پارامتر doctor الزامی است.'})

        return public_doctor_availability(doctor_id=doctor_id, day=date)
