from django.urls import path
from . import views


app_name = 'appointment'

urlpatterns = [
    # Available Times
    path('doctor/available-times/', views.ListAvailableTimeView.as_view(), name='available-times-list'),
    path('doctor/available-times/create/', views.CreateAvailableTimeView.as_view(), name='available-times-create'),
    path('doctor/available-times/update/<int:pk>/', views.UpdateDeleteAvailableTimeView.as_view(), name='available-times-update-delete'),

    # Appointments for patient
    path('patient/appointments/', views.ListAppointmentView.as_view(), name='appointments-list'),
    path('patient/appointments/create/', views.CreateAppointmentView.as_view(), name='appointments-create'),

    # Public doctor available times
    path('available-times/', views.PublicAvailableTimesForDoctorView.as_view(), name='public-doctor-available-times'),
]
