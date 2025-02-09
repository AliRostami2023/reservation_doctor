
from rest_framework.routers import DefaultRouter
from .views import AvailableTimeViewSet, AppointmentViewSet


router = DefaultRouter()
router.register('available_times', AvailableTimeViewSet, basename='available_times')
router.register('appointments', AppointmentViewSet, basename='appointments')

app_name = 'appointment'

urlpatterns = router.urls
