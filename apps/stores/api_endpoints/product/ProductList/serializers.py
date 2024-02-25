from rest_framework import serializers

from apps.stores.models import Product
from apps.stores.serializers import ProductUnitSerializer


class ProductListSerializer(serializers.ModelSerializer):
    unit = ProductUnitSerializer()
    label = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "label", "unit", "type", "is_active")
