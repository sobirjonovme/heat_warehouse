from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.stores.models import WarehouseProduct

from .serializers import WarehouseProductSerializer


class WarehouseProductListAPIView(ListAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(warehouse__stockman=self.request.user)
        queryset = queryset.select_related("warehouse", "product", "product__unit")
        return queryset


__all__ = ["WarehouseProductListAPIView"]
