from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from apps.orders.permissions import IsStockmanOrAdmin
from apps.stores.models import WarehouseProduct
from apps.users.models import UserRoles

from .serializers import WarehouseProductSerializer


class WarehouseProductListAPIView(ListAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductSerializer
    permission_classes = (IsStockmanOrAdmin,)

    filter_backends = (SearchFilter,)
    search_fields = ("product__name",)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.role == UserRoles.STOCKMAN:
            qs = qs.filter(warehouse__stockman=self.request.user)

        qs = qs.select_related("warehouse", "product", "product__unit")
        qs = qs.order_by("product__name")
        return qs


__all__ = ["WarehouseProductListAPIView"]
