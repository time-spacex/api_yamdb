from rest_framework import permissions


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object,
    admins or moderators to edit it.
    Assumes the model instance has an `author` attribute.
    """
    def has_object_permission(self, request, views, obj):
        return (
            (request.method in permissions.SAFE_METHODS)
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdmin(permissions.BasePermission):
    """permission allowing only the administrator to edit an object."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or (request.user.is_authenticated and request.user.is_admin)
        )