from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.stores.models import WarehouseProduct

from .serializers import WarehouseProductSerializer


class WarehouseProductListAPIView(ListAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (SearchFilter,)
    search_fields = ("product__name",)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(warehouse__stockman=self.request.user)
        queryset = queryset.select_related("warehouse", "product", "product__unit")
        queryset = queryset.order_by("product__name")
        return queryset


__all__ = ["WarehouseProductListAPIView"]
