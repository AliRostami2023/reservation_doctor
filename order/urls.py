from rest_framework.routers import DefaultRouter
from .views import AppointmentOrderViewSet, InvoiceViewSet, AdminAppointmentOrderViewSet


router = DefaultRouter()
router.register('orders', AppointmentOrderViewSet, basename='appointment-order')
router.register('invoices', InvoiceViewSet, basename='invoice')
router.register('list_appointment', AdminAppointmentOrderViewSet , basename='list_appointment')

app_name = 'order'

urlpatterns = router.urls
