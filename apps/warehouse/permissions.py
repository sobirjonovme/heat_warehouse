from rest_framework.permissions import BasePermission

from apps.users.models import UserRoles
from apps.warehouse.choices import OrderStatus


class IsStockman(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.role in [UserRoles.STOCKMAN, UserRoles.MAIN_STOCKMAN])


class CanOrderBeConfirmed(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(
            user.is_authenticated
            and user.role in [UserRoles.MAIN_STOCKMAN, UserRoles.ADMIN]
            and obj.status == OrderStatus.CREATED
        )


class CanOrderBeChecked(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(
            user.is_authenticated
            and user.role in [UserRoles.WATCHMAN, UserRoles.ADMIN]
            and obj.status == OrderStatus.CONFIRMED
        )


class CanOrderBeFinalChecked(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(
            user.is_authenticated
            and user.role in [UserRoles.MAIN_STOCKMAN, UserRoles.ADMIN]
            and obj.status == OrderStatus.DELIVERED
        )
