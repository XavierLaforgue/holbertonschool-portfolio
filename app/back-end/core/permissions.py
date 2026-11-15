from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Anyone can read; only administrators (is_staff) can write.

    Used for the reference data (difficulties, statuses, units,
    ingredients): every page needs to read it, but only the administration
    may change it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
