from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("register_patient", views.CreatePatientViewSet, basename='register_patient')
router.register("verify", views.VerifyCodeViewSet, basename='verify')
router.register("resend_code", views.ResendCodeViewSet, basename='resend_code')
router.register("request_reset_password", views.RequestPasswordResetViewSet, basename='request_reset_password')
router.register("confirm_reset_password", views.ConfirmResetPasswordViewSet, basename='confirm_reset_password')
router.register("register_doctor", views.CreateDoctorViewSet, basename='register_doctor')

app_name = 'auth'

urlpatterns = router.urls
