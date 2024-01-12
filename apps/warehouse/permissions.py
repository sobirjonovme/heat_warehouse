from rest_framework.permissions import BasePermission

from apps.users.models import UserRoles


class IsStockman(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.role in [UserRoles.STOCKMAN, UserRoles.MAIN_STOCKMAN])
