from django.contrib import admin
from .models import Appointment, AvailableTime, AppointmentDay


class AppointmentInline(admin.TabularInline):
    model = Appointment


class AvailableTimeInline(admin.TabularInline):
    model = AvailableTime


@admin.register(AppointmentDay)
class AppointmentDayAdmin(admin.ModelAdmin):
    list_display = ['day']
    inlines = [AvailableTimeInline, AppointmentInline]


@admin.register(AvailableTime)
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'is_active']
    list_filter = ['is_active']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'date', 'time', 'is_confirmed']
