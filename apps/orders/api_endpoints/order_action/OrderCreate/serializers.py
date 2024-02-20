from rest_framework import serializers

from apps.orders.models import Order, OrderItem


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "needed_amount",
        )
        ref_name = "OrderItemCreateSerializer"


class OrderCreateSerializer(serializers.ModelSerializer):
    items = ItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "items",
        )
        extra_kwargs = {
            "status": {"read_only": True},
        }

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
