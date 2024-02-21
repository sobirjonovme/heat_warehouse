from rest_framework import serializers

from apps.orders.serializers import UserShortSerializer
from apps.stores.models import Warehouse


class WarehouseListSerializer(serializers.ModelSerializer):
    stockman = UserShortSerializer()

    class Meta:
        model = Warehouse
        fields = ("id", "name", "stockman")
