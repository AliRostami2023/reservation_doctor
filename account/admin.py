from django.contrib import admin
from .models import User, Doctor, Patient, PasswordResetToken
from django.contrib.auth.models import Group


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'user_type', 'is_admin', 'is_active']
    list_filter = ['user_type', 'is_admin']
    search_fields = ['full_name']
    list_per_page = 20


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialty', 'experience_years', 'national_code', 'address']
    list_filter = ['specialty']
    search_fields = ['user', 'address', 'specialty']
    list_per_page = 20


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'national_code', 'address']
    search_fields = ['user', 'address']
    list_per_page = 20


@admin.register(PasswordResetToken)
class ResetPasswordAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created', 'is_used']
    search_fields = ['user']
    list_per_page = 20
