from rest_framework import viewsets, permissions
from ..models import Invoice
from ..serializers import InvoiceSerializer
from ..selectors.orders import invoices_for_user


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.prefetch_related('order')
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return invoices_for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save()
