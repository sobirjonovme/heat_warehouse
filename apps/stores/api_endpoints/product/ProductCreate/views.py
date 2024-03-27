from rest_framework.generics import CreateAPIView

from apps.orders.permissions import IsStockmanOrAdmin
from apps.stores.models import Product

from .serializers import ProductCreateSerializer


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = (IsStockmanOrAdmin,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


__all__ = ["ProductCreateAPIView"]
