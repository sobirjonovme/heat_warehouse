from rest_framework import serializers

from apps.orders.serializers import OrderDetailProductSerializer
from apps.stores.models import WarehouseProduct


class WarehouseProductSerializer(serializers.ModelSerializer):
    product = OrderDetailProductSerializer()
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
