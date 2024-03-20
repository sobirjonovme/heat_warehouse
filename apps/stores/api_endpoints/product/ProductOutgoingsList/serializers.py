from rest_framework import serializers

from apps.stores.models import Product
from apps.stores.serializers import ProductUnitSerializer


class ProductOutgoingsListSerializer(serializers.ModelSerializer):
    unit = ProductUnitSerializer()
    total_outgoings = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ("id", "name", "unit", "type", "is_active", "total_outgoings")
