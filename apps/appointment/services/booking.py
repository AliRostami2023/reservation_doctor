from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.appointment.models import Appointment, AppointmentDay, AvailableTime


@transaction.atomic
def create_patient_appointment(*, patient, doctor, day, time):
    """Reserve a time slot atomically to reduce concurrent double bookings."""
    appointment_day = AppointmentDay.objects.filter(day=day).first()
    if appointment_day is None:
        raise serializers.ValidationError(_('تاریخ موردنظر یافت نشد.'))

    available_slots = AvailableTime.objects.select_for_update().filter(
        doctor=doctor, date=appointment_day, start_time__lte=time,
        end_time__gte=time, is_active=True,
    )
    if not available_slots.exists():
        raise serializers.ValidationError(_('این زمان توسط پزشک در دسترس نیست.'))

    if Appointment.objects.filter(patient=patient, date=appointment_day, time=time).exists():
        raise serializers.ValidationError(_('شما قبلاً در این زمان نوبت گرفته‌اید.'))

    return Appointment.objects.create(
        patient=patient, doctor=doctor, date=appointment_day,
        time=time, is_confirmed=True,
    )
