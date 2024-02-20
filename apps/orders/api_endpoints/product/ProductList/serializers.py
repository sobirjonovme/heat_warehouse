from rest_framework import serializers

from apps.orders.models import Product
from apps.orders.serializers import ProductUnitSerializer


class ProductListSerializer(serializers.ModelSerializer):
    unit = ProductUnitSerializer()

    class Meta:
        model = Product
        fields = ("id", "name", "unit", "type", "in_stock", "is_active")
