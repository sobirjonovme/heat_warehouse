from rest_framework import serializers

from apps.stores.models import Product
from apps.stores.serializers import ProductUnitSerializer


class ProductListSerializer(serializers.ModelSerializer):
    unit = ProductUnitSerializer()

    class Meta:
        model = Product
        fields = ("id", "name", "unit", "type", "is_active")
