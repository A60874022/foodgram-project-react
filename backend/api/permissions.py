from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Дает полный доступ для авторов и админов
    """

    def has_object_permission(self, request, view, obj):
            return (request.user.is_superuser
                or obj.author == request.user)
