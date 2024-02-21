from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import DebtPayback, OrderItem

from .serializers import PaybackDebtSerializer


class PaybackDebtAPIView(CreateAPIView):
    queryset = DebtPayback.objects.all()
    serializer_class = PaybackDebtSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        order_item = get_object_or_404(OrderItem, pk=self.kwargs.get("order_item_id"))
        return order_item

    # override serializer method save
    def perform_create(self, serializer):
        order_item = self.get_object()
        serializer.save(order_item=order_item, user=self.request.user)


__all__ = ["PaybackDebtAPIView"]
