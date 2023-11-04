from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.IsAuthenticated):
    message = "Only the author can edit this article."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `author`.
        return obj.author == request.user

class IsCommenterOrReadOnly(permissions.IsAuthenticated):
    message = "Only the commenter can edit this comment."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `author`.
        return obj.user == request.user