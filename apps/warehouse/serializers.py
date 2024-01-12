from rest_framework import serializers

from apps.users.models import User
from apps.warehouse.models import Product, ProductUnit


class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = ("id", "name", "short_name")


class OrderDetailProductSerializer(serializers.ModelSerializer):
    unit = ProductUnitSerializer()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "unit",
        )


class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "role",
        )
