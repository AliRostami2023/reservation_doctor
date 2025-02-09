import django_filters
from .models import AppointmentOrder


class AppointmentOrderFilter(django_filters.FilterSet):
    national_code = django_filters.CharFilter(field_name="patient__user__national_code", lookup_expr='exact')
    tracking_code = django_filters.CharFilter(field_name="tracking_code", lookup_expr='exact')
    date = django_filters.DateFilter(field_name="date", lookup_expr='exact')

    class Meta:
        model = AppointmentOrder
        fields = ['national_code', 'tracking_code', 'date']
