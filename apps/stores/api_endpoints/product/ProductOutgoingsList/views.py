from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from apps.orders.choices import OrderStatus
from apps.orders.models import OrderItem
from apps.orders.permissions import IsStockmanOrAdmin
from apps.stores.models import Product
from apps.users.models import UserRoles

from .filters import DATE_FILTER_PARAMETERS, OrderItemFilter
from .serializers import ProductOutgoingsListSerializer


class ProductOutgoingsListAPIView(ListAPIView):
    serializer_class = ProductOutgoingsListSerializer
    permission_classes = (IsStockmanOrAdmin,)

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("type",)
    search_fields = ("name",)

    def get_queryset(self):
        user = self.request.user
        order_items = OrderItem.objects.filter(order__status=OrderStatus.FINAL_CHECKED)

        if user.role == UserRoles.STOCKMAN:
            order_items = order_items.filter(order__warehouse__stockman=user)

        order_items = OrderItemFilter(self.request.GET, queryset=order_items).qs
        order_items = order_items.annotate(
            total_amount=models.F("cash_amount") + models.F("card_amount") + models.F("debt_amount")
        )
        product_ids = set(order_items.values_list("product_id", flat=True))

        queryset = Product.objects.filter(is_active=True, id__in=product_ids)
        queryset = queryset.select_related("unit")
        queryset = queryset.order_by("name")
        queryset = queryset.annotate(
            total_outgoings=models.Subquery(
                order_items.filter(product_id=models.OuterRef("id"))
                .values("product_id")
                .annotate(total_money=models.Sum("total_amount"))
                .values("total_money")
            )
        )

        return queryset

    @swagger_auto_schema(manual_parameters=DATE_FILTER_PARAMETERS)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


__all__ = ["ProductOutgoingsListAPIView"]
