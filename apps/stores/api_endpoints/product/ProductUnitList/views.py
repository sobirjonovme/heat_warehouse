from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.stores.models import ProductUnit
from apps.stores.serializers import ProductUnitSerializer


class ProductUnitListAPIView(ListAPIView):
    queryset = ProductUnit.objects.order_by("name")
    serializer_class = ProductUnitSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (SearchFilter,)
    search_fields = ("name", "short_name")
    pagination_class = None


__all__ = ["ProductUnitListAPIView"]
