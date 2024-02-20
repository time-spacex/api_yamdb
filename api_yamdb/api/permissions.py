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
