from rest_framework import permissions

from .models import Profile


class IsAccountOwnerOrAdmin(permissions.BasePermission):
    """The account (or its profile) is the logged-in user's own, or the
    user is an administrator.

    DRF calls has_object_permission() once the object is found, i.e. for
    reading, changing or deleting one account or one profile.
    """

    def has_object_permission(self, request, view, obj):
        owner = obj.user if isinstance(obj, Profile) else obj
        return request.user.is_staff or owner == request.user
