from rest_framework import serializers
from .models import AppointmentOrder, Invoice


class AppointmentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentOrder
        fields = ['id', 'patient', 'doctor', 'appointment', 'tracking_code', 'status', 'create_at']
        read_only_fields = ['tracking_code', 'create_at']



class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'order', 'amount', 'description', 'create_at']
        read_only_fields = ['create_at']
