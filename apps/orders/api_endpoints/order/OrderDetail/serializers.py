from rest_framework import serializers

from apps.orders.models import Order, OrderItem
from apps.orders.serializers import UserShortSerializer
from apps.stores.models import Product
from apps.stores.serializers import WarehouseShortSerializer


class ProductSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source="unit.short_name", read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "unit", "type", "is_active")
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
            "cash_amount",
            "card_amount",
            "debt_amount",
        )
        ref_name = "OrderDetailOrderItemSerializer"


class OrderDetailSerializer(serializers.ModelSerializer):
    warehouse = WarehouseShortSerializer(read_only=True)
    ordered_by = UserShortSerializer(read_only=True)
    main_stockman = UserShortSerializer(read_only=True)
    supplier = UserShortSerializer(read_only=True)
    watchman = UserShortSerializer(read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "warehouse",
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
