from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.stores.models import Warehouse
from apps.users.models import UserRoles

from .serializers import WarehouseListSerializer


class WarehouseListAPIView(ListAPIView):
    serializer_class = WarehouseListSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("stockman",)

    def get_queryset(self):
        queryset = Warehouse.objects.filter(is_active=True)
        queryset = queryset.select_related("stockman")
        queryset = queryset.order_by("name")

        user = self.request.user
        if user.role in (UserRoles.ADMIN, UserRoles.MAIN_STOCKMAN):
            return queryset

        if user.role == UserRoles.STOCKMAN:
            return queryset.filter(stockman=user)

        # return empty queryset
        return queryset.none()


__all__ = ["WarehouseListAPIView"]
