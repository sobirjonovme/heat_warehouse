from rest_framework import serializers

from apps.orders.models import Product, ProductUnit
from apps.users.models import User


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
