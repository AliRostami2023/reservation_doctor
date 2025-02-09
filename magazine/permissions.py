from rest_framework.permissions import BasePermission


class IsAuthenticatedOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return request.user and request.user.is_staff