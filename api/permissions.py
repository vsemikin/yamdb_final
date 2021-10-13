from rest_framework import permissions


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    """The class defines the access rights to the resource."""

    def has_object_permission(self, request, view, obj):
        """The function provides access depending on the user's role."""
        return (
            (request.method in permissions.SAFE_METHODS)
            or (obj.author == request.user)
            or request.user.check_role
        )


class IsGetOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_staff and request.user.is_authenticated
