from rest_framework.generics import CreateAPIView

from apps.orders.permissions import IsStockman
from apps.stores.models import Product

from .serializers import ProductCreateSerializer


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = (IsStockman,)


__all__ = ["ProductCreateAPIView"]
