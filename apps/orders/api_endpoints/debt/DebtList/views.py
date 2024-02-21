from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.filters import OrderItemFilter
from apps.orders.models import OrderItem

from .serializers import DebtListSerializer


class DebtListAPIView(ListAPIView):
    serializer_class = DebtListSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderItemFilter

    def get_queryset(self):
        queryset = OrderItem.objects.filter(debt_amount__gt=0)
        queryset = queryset.select_related("product", "product__unit")
        queryset = queryset.order_by("-created_at")
        return queryset


__all__ = ["DebtListAPIView"]
