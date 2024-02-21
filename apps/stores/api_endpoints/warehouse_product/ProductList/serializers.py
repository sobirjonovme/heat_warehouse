from rest_framework import serializers

from apps.stores.models import WarehouseProduct
from apps.stores.serializers import ProductShortSerializer


class WarehouseProductSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer()
    warehouse = serializers.SerializerMethodField()

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
