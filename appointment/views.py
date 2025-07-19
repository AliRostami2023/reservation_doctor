from django.db import transaction
from django.utils.translation import gettext_lazy as _
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


class CreateAppointmentView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentCreateSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        patient = self.request.user.patient_user
        doctor = serializer.validated_data['doctor']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']

        with transaction.atomic():
            try:
                appointment_day = AppointmentDay.objects.get(day=date['day'])
            except AppointmentDay.DoesNotExist:
                raise serializers.ValidationError(_('تاریخ موردنظر یافت نشد.'))

            available = AvailableTime.objects.select_for_update().filter(
                doctor=doctor,
                date=appointment_day,
                start_time__lte=time,
                end_time__gte=time,
                is_active=True
            )
            if not available.exists():
                raise serializers.ValidationError(_('این زمان توسط پزشک در دسترس نیست.'))

            if Appointment.objects.filter(patient=patient, date=appointment_day, time=time).exists():
                raise serializers.ValidationError(_('شما قبلاً در این زمان نوبت گرفته‌اید.'))

            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=appointment_day,
                time=time,
                is_confirmed=True
            )



class ListAppointmentView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = PatientAppointmentListSerializer
    permission_classes = [IsAuthenticated, IsPatient]
    

class PublicAvailableTimesForDoctorView(generics.ListAPIView):
    serializer_class = AppointmentListSerializer

    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor')
        date = self.request.query_params.get('date')

        if not doctor_id:
            raise serializers.ValidationError({'doctor': 'پارامتر doctor الزامی است.'})

        queryset = AvailableTime.objects.filter(is_active=True, doctor_id=doctor_id)

        if date:
            queryset = queryset.filter(date=date)

        return queryset.order_by('date', 'start_time')
    