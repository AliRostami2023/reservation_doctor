from rest_framework import permissions

class IsPatientOrReadOnly(permissions.BasePermission):
    """
    - بیماران فقط می‌توانند نوبت خود را ببینند و تغییر دهند.
    - پزشکان و منشی‌ها می‌توانند تمام نوبت‌ها را مشاهده کنند.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.patient.user == request.user

class IsDoctorOrReceptionist(permissions.BasePermission):
    """
    - پزشک یا منشی پزشک اجازه دیدن تمام نوبت‌ها را دارند.
    - بیماران فقط نوبت‌های خود را می‌بینند.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            hasattr(request.user) or request.user.is_staff
        )
