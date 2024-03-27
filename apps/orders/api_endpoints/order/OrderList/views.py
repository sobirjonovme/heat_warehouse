# from django.db.models import Case, DecimalField, F, Sum, Value, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.orders.models import Order
from apps.orders.permissions import IsStockmanOrAdmin
# from apps.orders.choices import OrderStatus
from apps.users.models import UserRoles

from .serializers import OrderListSerializer


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (IsStockmanOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {
        "created_at": ["gte", "lte"],
        "status": ["exact"],
        "ordered_by": ["exact"],
        "main_stockman": ["exact"],
        "supplier": ["exact"],
        "watchman": ["exact"],
    }

    def get_queryset(self):
        user = self.request.user

        qs = Order.objects.order_by("-created_at")
        if user.role == UserRoles.STOCKMAN:
            qs = qs.filter(warehouse__stockman=self.request.user)

        # if object status CHECKED, then annotate total_money
        # in other cases, annotate total_money = 0
        # total money = sum of all items' prices
        # queryset = queryset.annotate(
        #     total_money=Sum(
        #         Case(
        #             # Calculate sum only if status is 'FINAL_CHECKED'
        #             When(status=OrderStatus.FINAL_CHECKED, then="items__price"),
        #             default=Value(0),  # Default value of total_money when status is not 'done'
        #             output_field=DecimalField(),  # Specify the output field type
        #         )
        #     )
        # )

        qs = qs.select_related("warehouse", "ordered_by", "main_stockman", "supplier", "watchman")
        return qs


__all__ = ["OrderListAPIView"]
