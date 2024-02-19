from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """permission allowing only the administrator to edit an object."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            (request.user.role == 'admin') or request.user.is_superuser
        )
