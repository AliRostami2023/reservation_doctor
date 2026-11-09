from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from ..models import AppointmentOrder
from ..serializers import AppointmentOrderSerializer
from ..filters import AppointmentOrderFilter
from ..permissions import IsDoctorOrReceptionist, IsPatientOrReadOnly
from ..selectors.orders import orders_for_user


class AppointmentOrderViewSet(viewsets.ModelViewSet):
    queryset = AppointmentOrder.objects.select_related('patient', 'doctor', 'appointment')
    serializer_class = AppointmentOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrReadOnly | IsDoctorOrReceptionist]


    def get_queryset(self):
        return orders_for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class AdminAppointmentOrderViewSet(viewsets.ModelViewSet):
    queryset = AppointmentOrder.objects.all()
    serializer_class = AppointmentOrderSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AppointmentOrderFilter
