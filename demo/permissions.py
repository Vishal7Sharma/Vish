from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission so only author can only delete/update his/her posts
    """

    def has_object_permission(self, request, view, obj):
        """Read permissions are allowed to any request, We will always allow Get, head and options requests"""
        if request.method in permissions.SAFE_METHODS:
            return True

        # write permissions are only to author
        return obj.author == request.user
