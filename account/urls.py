from django.urls import path
from . import views


app_name = 'auth'

urlpatterns = [
    path('register_patient/', views.CreatePatientAPIView.as_view(), name='register_patient'),
    path('verify_patient/', views.VerifyCodeAPIView.as_view(), name='verify_patient'),
    path('resend_code/', views.ResendCodeAPIView.as_view(), name='resend_code'),
    path('request_reset_password/', views.RequestPasswordResetAPIView.as_view(), name='request_reset_password'),
    path('reset-password/<uuid:token>/', views.ConfirmResetPasswordViewSet.as_view(), name='reset-password'),
    path('register_doctor/', views.CreateDoctorAPIView.as_view(), name='register_doctor'),
    path('list_doctor/', views.ListDoctorProfileAPIView.as_view(), name='list_doctor'),
    path('profile_doctor/<int:pk>/', views.RetriveDoctorProfileAPIView.as_view(), name='profile_doctor'),
    path('profile_doctor/update/<int:pk>/', views.UpdateDoctorProfileAPIView.as_view(), name='update_doctor'),
    path('profile_patient/<int:pk>/', views.RetrivePatientProfileAPIView.as_view(), name='profile_patient'),
    path('list_profile_patient', views.ListPatientProfileAPIView.as_view(), name='list_profile_patient'),
    path('profile_patient/update/<int:pk>/', views.UpdatePatientProfileAPIView.as_view(), name='update_profile_patient'),
]
