from django.db.models import Case, DecimalField, Sum, Value, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.warehouse.choices import OrderStatus
from apps.warehouse.models import Order

from .serializers import OrderListSerializer


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {
        "created_at": ["gte", "lte"],
        "status": ["exact"],
    }

    def get_queryset(self):
        queryset = Order.objects.order_by("-created_at")

        # if object status CHECKED, then annotate total_money
        # in other cases, annotate total_money = 0
        # total money = sum of all items' prices
        queryset = queryset.annotate(
            total_money=Sum(
                Case(
                    # Calculate sum only if status is 'FINAL_CHECKED'
                    When(status=OrderStatus.FINAL_CHECKED, then="items__price"),
                    default=Value(0),  # Default value of total_money when status is not 'done'
                    output_field=DecimalField(),  # Specify the output field type
                )
            )
        )
        return queryset


__all__ = ["OrderListAPIView"]
