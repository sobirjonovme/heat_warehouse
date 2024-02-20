from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.stores.models import WarehouseProduct, WarehouseProductUsage

from .serializers import UseWarehouseProductSerializer


class UseWarehouseProductAPIView(CreateAPIView):
    queryset = WarehouseProductUsage.objects.all()
    serializer_class = UseWarehouseProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        warehouse_product = get_object_or_404(WarehouseProduct, pk=self.kwargs.get("pk"))
        return warehouse_product

    # override serializer method save
    def perform_create(self, serializer):
        warehouse_product = self.get_object()
        serializer.save(warehouse_product=warehouse_product)


__all__ = ["UseWarehouseProductAPIView"]
