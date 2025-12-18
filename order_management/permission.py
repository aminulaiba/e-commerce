from rest_framework.permissions import BasePermission


class IsOrderManagement(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='Order Management System').exists()
        )