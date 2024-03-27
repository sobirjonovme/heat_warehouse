from rest_framework.generics import ListAPIView

from apps.orders.models import DebtPayback
from apps.orders.permissions import IsStockmanOrAdmin
from apps.users.models import UserRoles

from .serializers import DebtPaybackListSerializer


class DebtPaybackListAPIView(ListAPIView):
    serializer_class = DebtPaybackListSerializer
    permission_classes = (IsStockmanOrAdmin,)

    def get_queryset(self):
        user = self.request.user
        queryset = DebtPayback.objects.all()

        if user.role == UserRoles.STOCKMAN:
            queryset = queryset.filter(order_item__order__warehouse__stockman=user)

        queryset = queryset.select_related("order_item", "order_item__product", "order_item__product__unit")
        return queryset


__all__ = ["DebtPaybackListAPIView"]
