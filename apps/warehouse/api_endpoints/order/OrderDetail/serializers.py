from rest_framework import serializers

from apps.warehouse.models import Order, OrderItem, Product
from apps.warehouse.serializers import OrderUserSerializer


class ProductSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source="unit.short_name", read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "unit", "type", "in_stock", "is_active")
        ref_name = "OrderDetailProductSerializer"


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "needed_amount",
            "delivered_amount",
            "price",
        )
        ref_name = "OrderDetailOrderItemSerializer"


class OrderDetailSerializer(serializers.ModelSerializer):
    ordered_by = OrderUserSerializer(read_only=True)
    main_stockman = OrderUserSerializer(read_only=True)
    supplier = OrderUserSerializer(read_only=True)
    watchman = OrderUserSerializer(read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "ordered_by",
            "main_stockman",
            "supplier",
            "watchman",
            "created_at",
            "items",
        )

    def get_items(self, obj):
        items = obj.items.all()
        items = items.select_related("product", "product__unit")
        return OrderItemSerializer(items, many=True).data
