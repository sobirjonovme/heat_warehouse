from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.warehouse.models import Product

from .serializers import ProductListSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("type",)

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        queryset = queryset.select_related("unit")
        queryset = queryset.order_by("name")
        return queryset


__all__ = ["ProductListAPIView"]
