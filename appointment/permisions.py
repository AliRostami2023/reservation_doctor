from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    message = "فقط پزشکان می‌توانند به این بخش دسترسی داشته باشند."


    def has_permission(self, request, view):
        return hasattr(request.user, 'doctor_profile')


class IsPatient(BasePermission):
    message = "فقط بیماران می‌توانند به این بخش دسترسی داشته باشند."


    def has_permission(self, request, view):
        return hasattr(request.user, 'patient_user')
