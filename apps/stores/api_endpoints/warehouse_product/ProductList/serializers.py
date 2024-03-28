from rest_framework import serializers

from apps.common.services.common import remove_exponent_from_decimal
from apps.stores.models import WarehouseProduct
from apps.stores.serializers import ProductShortSerializer


class WarehouseProductSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer()
    warehouse = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = WarehouseProduct
        fields = (
            "id",
            "warehouse",
            "product",
            "quantity",
        )
        ref_name = "WarehouseProductListSerializer"

    def get_warehouse(self, obj):
        return obj.warehouse.name if obj.warehouse else None

    def get_quantity(self, obj):
        if obj.quantity is None:
            return None

        quantity = remove_exponent_from_decimal(obj.quantity)
        return str(quantity)
