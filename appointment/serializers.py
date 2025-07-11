from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import AvailableTime, Appointment, AppointmentDay
from account.models import Doctor


class AppointmentDaySimpleSerializer(serializers.ModelSerializer):
    day = serializers.DateField(required=True, format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        model = AppointmentDay
        fields = ['day']


class AvailableTimeCreateSerializer(serializers.ModelSerializer):
    date = AppointmentDaySimpleSerializer(required=True, label="تاریخ")
    doctor = serializers.CharField(source='doctor.user.full_name', read_only=True)

    start_time = serializers.TimeField(
        required=True,
        label='ساعت شروع',
        format="%H:%M"
    )
    end_time = serializers.TimeField(
        required=True,
        label='ساعت پایان',
        format="%H:%M"
    )

    class Meta:
        model = AvailableTime
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_active']

    def validate(self, attrs):
        doctor = self.context['request'].user.doctor_profile
        date_data = attrs.get("date")
        day = date_data.get("day")
        start = attrs.get("start_time")
        end = attrs.get("end_time")

        if start >= end:
            raise serializers.ValidationError("زمان شروع باید قبل از زمان پایان باشد.")

        overlap = AvailableTime.objects.filter(
            doctor=doctor,
            date__day=day,
            start_time__lt=end,
            end_time__gt=start,
        )

        if overlap.exists():
            raise serializers.ValidationError("این بازه زمانی با بازه دیگری تداخل دارد.")

        return attrs

    

class AvailableTimeListSerializer(serializers.ModelSerializer):
    date = serializers.CharField(source="date.day")
    doctor = serializers.CharField(source='doctor.user.full_name', read_only=True)

    class Meta:
        model = AvailableTime
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_active']

    

class AvailableTimeUpdateSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.user.full_name', read_only=True)
    
    class Meta:
        model = AvailableTime
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_active']
    


class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        required=True,
        label='پزشک'
    )
    date = serializers.PrimaryKeyRelatedField(
        queryset=AppointmentDay.objects.all(),
        required=True,
        label='تاریخ'
    )
    time = serializers.TimeField(
        required=True,
        label='ساعت',
        format="%H:%M"
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']

    def validate(self, attrs):
        request = self.context['request']
        patient = getattr(request.user, 'patient_user', None)
        doctor = attrs.get('doctor')
        date = attrs.get('date')
        time = attrs.get('time')

        if not patient:
            raise serializers.ValidationError(_("اطلاعات بیمار یافت نشد."))

        available = AvailableTime.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lte=time,
            end_time__gte=time,
            is_active=True
        )
        if not available.exists():
            raise serializers.ValidationError(_('این زمان توسط پزشک در دسترس نیست.'))

        if Appointment.objects.filter(patient=patient, date=date, time=time).exists():
            raise serializers.ValidationError(_('شما قبلاً در این زمان نوبت گرفته‌اید.'))

        return attrs
    

class AppointmentListSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.user.full_name', read_only=True)
    patient = serializers.CharField(source='patient.user.full_name', read_only=True)
    date = serializers.DateField(source='available_time.date', read_only=True)
    time = serializers.TimeField(source='available_time.start_time', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
