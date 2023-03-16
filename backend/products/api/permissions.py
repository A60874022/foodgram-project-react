from rest_framework import permissions 

 
 
class IsAuthenticatedOrReadOnly(permissions.BasePermission): 
    """ 
    Дает доступ к безопасным методам для неавторизованных пользователей, 
    и полный доступ для авторизованных и админов 
    """ 
    def has_permission(self, request, view): 
        return ( 
            request.method in permissions.SAFE_METHODS 
            or request.user.is_authenticated 
        ) 
    def has_object_permission(self, request, view, obj): 
        if request.user and request.user.is_authenticated: 
            return (request.user.is_superuser 
                    or obj.author == request.user) 
        return False 
