from datetime import datetime

from django_filters import rest_framework as filters
from drf_yasg import openapi

from apps.orders.models import OrderItem


class OrderItemFilter(filters.FilterSet):
    from_date = filters.DateFilter(method="filter_from_date", field_name="order__created_at")
    to_date = filters.DateFilter(method="filter_to_date", field_name="order__created_at")

    class Meta:
        model = OrderItem
        fields = ("from_date", "to_date")

    def filter_from_date(self, queryset, name, value):
        from_time = datetime.strptime(f"{value} 00:00:00 +0000", "%Y-%m-%d %H:%M:%S %z")
        return queryset.filter(order__created_at__gte=from_time)

    def filter_to_date(self, queryset, name, value):
        to_time = datetime.strptime(f"{value} 23:59:59 +0000", "%Y-%m-%d %H:%M:%S %z")
        return queryset.filter(order__created_at__lte=to_time)


DATE_FILTER_PARAMETERS = [
    openapi.Parameter("from_date", openapi.IN_QUERY, type=openapi.FORMAT_DATE),
    openapi.Parameter("to_date", openapi.IN_QUERY, type=openapi.FORMAT_DATE),
]
