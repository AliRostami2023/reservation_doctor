from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("register_patient", views.CreatePatientViewSet, basename='register_patient')
router.register("verify", views.VerifyCodeViewSet, basename='verify')
router.register("resend_code", views.ResendCodeViewSet, basename='resend_code')
router.register("request_reset_password", views.RequestPasswordResetViewSet, basename='reset_password')
router.register("confirm_reset_password", views.ConfirmResetPasswordViewSet, basename='confirm_reset_password')
router.register("register_doctor", views.CreateDoctorViewSet, basename='register_doctor')
router.register("patient_profile", views.PatientProfileViewSet, basename='patient_profile')
router.register("doctor_profile", views.DoctorProfileViewSet, basename='doctor_profile')

app_name = 'auth'

urlpatterns = router.urls + [
    path('reset-password/<uuid:token>/', views.ConfirmResetPasswordViewSet.as_view({'post': 'create'}), name='reset-password'),
]
