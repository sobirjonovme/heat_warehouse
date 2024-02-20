from rest_framework import serializers

from apps.stores.models import WarehouseProduct, WarehouseProductUsage


class UseWarehouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProductUsage
        fields = (
            "id",
            "quantity",
            "to_warehouse",
            "comment",
        )

    def create(self, validated_data):
        instance = super().create(validated_data)

        if instance.to_warehouse:
            # add product amount to another warehouse
            product = instance.warehouse_product.product
            target_warehouse_product, _ = WarehouseProduct.objects.get_or_create(
                warehouse=instance.to_warehouse, product=product
            )
            target_warehouse_product.quantity += instance.quantity
            target_warehouse_product.save()

        # remove product amount from current warehouse
        warehouse_product = instance.warehouse_product
        warehouse_product.quantity -= instance.quantity
        warehouse_product.save()

        return instance
