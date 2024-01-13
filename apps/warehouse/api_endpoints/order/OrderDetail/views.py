from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.warehouse.models import Order

from .serializers import OrderDetailSerializer


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)


__all__ = ["OrderDetailAPIView"]
