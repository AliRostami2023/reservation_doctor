from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import AppointmentOrder, Invoice
from .serializers import AppointmentOrderSerializer, InvoiceSerializer
from .filters import AppointmentOrderFilter
from .permissions import IsDoctorOrReceptionist, IsPatientOrReadOnly


class AppointmentOrderViewSet(viewsets.ModelViewSet):
    queryset = AppointmentOrder.objects.select_related('patient', 'doctor', 'appointment')
    serializer_class = AppointmentOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrReadOnly | IsDoctorOrReceptionist]


    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient'):
            return self.queryset.filter(patient__user=user)
        elif hasattr(user, 'doctor'):
            return self.queryset.filter(doctor__user=user)
        elif user.is_staff:
            return self.queryset
        return AppointmentOrder.objects.none()

    def perform_create(self, serializer):
        serializer.save()



class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.prefetch_related('order')
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient'):
            return self.queryset.filter(order__patient__user=user)
        elif hasattr(user, 'doctor'):
            return self.queryset.filter(order__doctor__user=user)
        elif user.is_staff:
            return self.queryset
        return Invoice.objects.none()

    def perform_create(self, serializer):
        serializer.save()



class AdminAppointmentOrderViewSet(viewsets.ModelViewSet):
    queryset = AppointmentOrder.objects.all()
    serializer_class = AppointmentOrderSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AppointmentOrderFilter

