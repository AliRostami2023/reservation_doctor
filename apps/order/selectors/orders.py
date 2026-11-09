from apps.order.models import AppointmentOrder, Invoice


def orders_for_user(user):
    queryset = AppointmentOrder.objects.select_related(
        'patient__user', 'doctor__user', 'appointment__date'
    )
    if hasattr(user, 'patient_user'):
        return queryset.filter(patient__user=user)
    if hasattr(user, 'doctor_profile'):
        return queryset.filter(doctor__user=user)
    if user.is_staff:
        return queryset
    return queryset.none()


def invoices_for_user(user):
    queryset = Invoice.objects.select_related(
        'order__patient__user', 'order__doctor__user', 'order__appointment__date'
    )
    if hasattr(user, 'patient_user'):
        return queryset.filter(order__patient__user=user)
    if hasattr(user, 'doctor_profile'):
        return queryset.filter(order__doctor__user=user)
    if user.is_staff:
        return queryset
    return queryset.none()
