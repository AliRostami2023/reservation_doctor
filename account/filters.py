import django_filters
from django.db.models import Q
from .models import Doctor


class DoctorFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='جستجو')

    class Meta:
        model = Doctor
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(user__full_name__icontains=value) |
            Q(specialty__icontains=value)
        )
    