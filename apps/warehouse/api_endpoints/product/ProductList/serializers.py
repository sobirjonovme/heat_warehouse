from rest_framework import serializers

from apps.warehouse.models import Product
from apps.warehouse.serializers import ProductUnitSerializer


class ProductListSerializer(serializers.ModelSerializer):
    unit = ProductUnitSerializer()

    class Meta:
        model = Product
        fields = ("id", "name", "unit", "type", "in_stock", "is_active")
