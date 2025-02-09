from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import AvailableTime, Appointment, AppointmentDay
from .mixins import PersianDateMixin


class AvailableTimSerializer(PersianDateMixin, serializers.ModelSerializer):
    date = serializers.PrimaryKeyRelatedField(
        queryset=AppointmentDay.objects.all(),
        required=True,
        label="تاریخ"
    )

    class Meta:
        model = AvailableTime
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_active']
        read_only_fields = ['doctor']

    def validate(self, attrs):
        doctor = self.context['request'].user.doctor_profile
        date = attrs.get("date")
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")


        overlapping_time = AvailableTime.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )

        if overlapping_time.exists():
            raise serializers.ValidationError(_("این بازه زمانب با زمان های موجود تداخل دارد"))
        
        return attrs
    
    def create(self, validated_data):
        doctor = self.context['request'].user.doctor
        validated_data['doctor'] = doctor
        return super().create(validated_data)
    


class AppointmentSerializer(PersianDateMixin, serializers.ModelSerializer):
    date = serializers.PrimaryKeyRelatedField(
        queryset=AppointmentDay.objects.all(),
        required=True,
        label='تاریخ',
    )
    time = serializers.TimeField(required=True, label='ساعت')

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time', 'is_confirmed']
        read_only_fields = ['doctor', 'patient', 'is_confirmed']

    def validate(self, attrs):
        patient = self.context['request'].user.patient_user
        doctor = self.context['request'].user.doctor_profile
        date = attrs.get('date')
        time = attrs.get('time')

        available_time = AvailableTime.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lte=time,
            end_time__gte=time,
            is_active=True,
        )
        if not available_time.exists():
            raise serializers.ValidationError(_('این زمان توسط پزشک در دسترس نیست.'))

        if Appointment.objects.filter(patient=patient, date=date, time=time).exists():
            raise serializers.ValidationError(_('شما قبلاً در این زمان نوبت گرفته‌اید.'))

        return attrs

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user.patient_user
        return super().create(validated_data)
    