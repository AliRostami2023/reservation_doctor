from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import AvailableTime, Appointment, AppointmentDay
from .mixins import PersianDateMixin
from account.models import Doctor


class AvailableTimeCreateSerializer(PersianDateMixin, serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_active']
        read_only_fields = ['doctor']

    def validate(self, attrs):
        doctor = self.context['request'].user.doctor_profile
        date = attrs.get("date")
        start = attrs.get("start_time")
        end = attrs.get("end_time")

        if start >= end:
            raise serializers.ValidationError("زمان شروع باید قبل از زمان پایان باشد.")

        overlap = AvailableTime.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lt=end,
            end_time__gt=start,
        )

        if overlap.exists():
            raise serializers.ValidationError("این بازه زمانی با بازه دیگری تداخل دارد.")

        return attrs

    def create(self, validated_data):
        validated_data['doctor'] = self.context['request'].user.doctor_profile
        return super().create(validated_data)
    

class AvailableTimeListSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = AvailableTime
        fields = ['id', 'date', 'start_time', 'end_time', 'is_active']
        read_only_fields = ['doctor']

    def get_date(self, obj):
        return obj.date.strftime('%Y/%m/%d')
    

class AvailableTimeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        fields = ['id', 'date', 'start_time', 'end_time', 'is_active']
        read_only_fields = ['doctor']
    


class AppointmentCreateSerializer(PersianDateMixin, serializers.ModelSerializer):
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

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user.patient_user
        return super().create(validated_data)
    

class AppointmentListSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.user.full_name', read_only=True)
    patient = serializers.CharField(source='patient.user.full_name', read_only=True)
    date = serializers.DateField(source='available_time.date', read_only=True)
    time = serializers.TimeField(source='available_time.start_time', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
