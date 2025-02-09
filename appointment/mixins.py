import jdatetime
from rest_framework import serializers


class PersianDateMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, value in representation.items():
            if isinstance(value, str):
                try:
                    date = serializers.DateField().to_internal_value(value)
                    jalali_date = jdatetime.date.fromgregorian(date=date)
                    representation[field_name] = jalali_date.strftime("%Y/%m/%d")
                except Exception:
                    try:
                        time = serializers.TimeField().to_internal_value(value)
                        representation[field_name] = time.strftime("%H:%M")
                    except Exception:
                        pass
        return representation
