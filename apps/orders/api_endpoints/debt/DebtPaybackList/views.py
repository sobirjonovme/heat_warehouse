from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import DebtPayback

from .serializers import DebtPaybackListSerializer


class DebtPaybackListAPIView(ListAPIView):
    serializer_class = DebtPaybackListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = DebtPayback.objects.all()
        queryset = queryset.select_related("order_item", "order_item__product", "order_item__product__unit")
        return queryset


__all__ = ["DebtPaybackListAPIView"]
