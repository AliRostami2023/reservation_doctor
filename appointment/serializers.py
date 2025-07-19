from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from datetime import datetime, date as datetime_date, time as datetime_time
from account.models import Doctor
from .models import AvailableTime, Appointment, AppointmentDay


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
    date = serializers.DateField(source="date.day")
    doctor = serializers.CharField(source='doctor.user.full_name', read_only=True)

    class Meta:
        model = AvailableTime
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_active']

    

class AvailableTimeUpdateSerializer(serializers.ModelSerializer):
    date = serializers.CharField(source="date.day")
    doctor = serializers.CharField(source='doctor.user.full_name', read_only=True)
    
    class Meta:
        model = AvailableTime
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_active']

    def update(self, instance, validated_data):
        day_value = validated_data.pop('date', {}).get('day', None)

        if day_value:
            if isinstance(day_value, str):
                day_value = datetime.strptime(day_value, "%Y-%m-%d").date()

            appointment_day, created = AppointmentDay.objects.get_or_create(day=day_value)

            instance.date = appointment_day

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    


class AppointmentCreateSerializer(serializers.ModelSerializer):
    date = AppointmentDaySimpleSerializer(required=True, label="تاریخ")
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        required=True,
        label='پزشک'
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
        date_data = attrs.get("date")
        day = date_data.get("day")
        time = attrs.get('time')

        if not patient:
            raise serializers.ValidationError(_("اطلاعات بیمار یافت نشد."))

        available = AvailableTime.objects.filter(
            doctor=doctor,
            date__day=day,
            start_time__lte=time,
            end_time__gte=time,
            is_active=True
        )
        if not available.exists():
            raise serializers.ValidationError(_('این زمان توسط پزشک در دسترس نیست.'))

        if Appointment.objects.filter(patient=patient, date__day=day, time=time).exists():
            raise serializers.ValidationError(_('شما قبلاً در این زمان نوبت گرفته‌اید.'))

        return attrs
    

class AppointmentListSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.user.full_name', read_only=True)
    date = serializers.DateField(source='date.day', read_only=True)

    class Meta:
        model = AvailableTime
        fields = ['id' ,'doctor', 'date', 'start_time', 'end_time', 'is_active']


class PatientAppointmentListSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.user.full_name', read_only=True)
    patient = serializers.CharField(source='patient.user.full_name')
    date = serializers.DateField(source='date.day', read_only=True)
    days_until_appointment = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time', 'is_confirmed', 'days_until_appointment']

    def get_days_until_appointment(self, obj):
        appointment_date = obj.date.day  # type: datetime.date
        appointment_time = obj.time      # type: datetime.time

        appointment_datetime = datetime.combine(appointment_date, appointment_time)

        now = datetime.now()

        delta = appointment_datetime - now

        if delta.total_seconds() > 0:
            days = delta.days
            hours = delta.seconds // 3600 
            
            if days > 0:
                return f"{days} روز و {hours} ساعت مانده به نوبت شما"
            elif hours > 0:
                return f"{hours} ساعت مانده به نوبت شما"
            else:
                minutes = (delta.seconds % 3600) // 60
                return f"{minutes} دقیقه مانده به نوبت شما"
        else:
            return "نوبت شما گذشته است"
