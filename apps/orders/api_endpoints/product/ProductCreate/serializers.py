from rest_framework import serializers

from apps.orders.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "unit", "type")
        extra_kwargs = {
            "unit": {"required": True},
        }
