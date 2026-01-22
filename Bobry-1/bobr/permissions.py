from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Nasze reguły:
    - Każdy (też niezalogowani) mogą CZYTAĆ (GET).
    - Tylko Admin może ZAPISYWAĆ/USUWAĆ (POST, PUT, DELETE).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_staff