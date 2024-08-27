from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the profile.
        return obj.profile.user == request.user

class IsRoleGSOrPresident(BasePermission):
    """
    Custom permission to only allow users with the role of 'GS' or 'President'.
    """
    def has_permission(self, request, view):
        return request.user.role in ['GS', 'President']
