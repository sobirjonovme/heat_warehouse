from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.orders.filters import OrderItemFilter
from apps.orders.models import OrderItem
from apps.orders.permissions import IsStockmanOrAdmin
from apps.users.models import UserRoles

from .serializers import DebtListSerializer


class DebtListAPIView(ListAPIView):
    serializer_class = DebtListSerializer
    permission_classes = (IsStockmanOrAdmin,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderItemFilter

    def get_queryset(self):
        user = self.request.user
        qs = OrderItem.objects.filter(debt_amount__gt=0)

        if user.role == UserRoles.STOCKMAN:
            qs = qs.filter(order__warehouse__stockman=self.request.user)

        qs = qs.select_related("product", "product__unit")
        qs = qs.order_by("-created_at")
        return qs


__all__ = ["DebtListAPIView"]
