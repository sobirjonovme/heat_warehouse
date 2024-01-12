from rest_framework.generics import CreateAPIView

from apps.warehouse.permissions import IsStockman

from .serializers import ProductCreateSerializer


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = (IsStockman,)


__all__ = ["ProductCreateAPIView"]
