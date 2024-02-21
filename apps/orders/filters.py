from django_filters import rest_framework as filters
from drf_yasg import openapi

from .models import OrderItem


class OrderItemFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name="created_at__date", lookup_expr="gte")
    to_date = filters.DateFilter(field_name="created_at__date", lookup_expr="lte")
    only_active = filters.BooleanFilter(field_name="only_active", method="filter_only_active")

    class Meta:
        model = OrderItem
        filterset_fields = ()
        fields = ("from_date", "to_date", "only_active", "order__warehouse", "order__warehouse__stockman")

    def filter_only_active(self, queryset, name, value):
        if value:
            return queryset.filter(remain_debt__gt=0)
        return queryset


DATE_FILTER_PARAMETERS = [
    openapi.Parameter("from_date", openapi.IN_QUERY, type=openapi.FORMAT_DATE),
    openapi.Parameter("to_date", openapi.IN_QUERY, type=openapi.FORMAT_DATE),
]
