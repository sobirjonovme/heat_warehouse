from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.stores.models import Product

from .serializers import ProductListSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("type",)
    search_fields = ("name",)
    pagination_class = None

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        queryset = queryset.select_related("unit")
        queryset = queryset.order_by("name")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "count": queryset.count(),
            "next": None,
            "previous": None,
            "results": serializer.data,
        }
        return Response(data)


__all__ = ["ProductListAPIView"]
