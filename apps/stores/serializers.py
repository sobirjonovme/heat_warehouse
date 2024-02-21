from rest_framework import serializers

from apps.stores.models import Product, ProductUnit


class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = ("id", "name", "short_name")


class ProductShortSerializer(serializers.ModelSerializer):
    unit = ProductUnitSerializer()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "unit",
        )
