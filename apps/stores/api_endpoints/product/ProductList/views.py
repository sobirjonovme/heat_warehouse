from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.stores.models import Product

from .serializers import ProductListSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("type",)
    search_fields = ("name",)

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        queryset = queryset.select_related("unit")
        queryset = queryset.order_by("name")
        return queryset


__all__ = ["ProductListAPIView"]
