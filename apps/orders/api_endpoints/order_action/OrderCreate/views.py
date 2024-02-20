from rest_framework.generics import CreateAPIView

from apps.orders.models import Order
from apps.orders.permissions import IsStockman

from .serializers import OrderCreateSerializer


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (IsStockman,)

    def perform_create(self, serializer):
        serializer.save(ordered_by=self.request.user)


__all__ = ["OrderCreateAPIView"]
