from rest_framework import exceptions, permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAuthorOrAdminOrReadOnly(permissions.DjangoModelPermissions):
    """
    Дает доступ к безопасным методам для неавторизованных пользователей,
    и полный доступ для авторизованных и админов
    """
    perms_map = {
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def get_required_permissions(self, method, model_cls, request):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }

        if (method not in self.perms_map or
           request.method in permissions.SAFE_METHODS):
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            return (request.user.is_superuser
                    or obj.author == request.user)
        return False
