from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = "Only the author can edit this article."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user