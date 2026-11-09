from apps.appointment.models import AvailableTime


def public_doctor_availability(*, doctor_id, day=None):
    queryset = AvailableTime.objects.filter(is_active=True, doctor_id=doctor_id)
    if day:
        queryset = queryset.filter(date__day=day)
    return queryset.select_related('doctor__user', 'date').order_by('date__day', 'start_time')
