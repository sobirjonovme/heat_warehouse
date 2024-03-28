from rest_framework import serializers

from apps.common.services.common import remove_exponent_from_decimal
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
    needed_amount = serializers.SerializerMethodField()
    delivered_amount = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "comment",
            "needed_amount",
            "delivered_amount",
            "cash_amount",
            "card_amount",
            "debt_amount",
            "remain_debt",
            "payment_comment",
        )
        ref_name = "OrderDetailOrderItemSerializer"

    def get_needed_amount(self, obj):
        if obj.needed_amount is None:
            return None

        needed_amount = remove_exponent_from_decimal(obj.needed_amount)
        return str(needed_amount)

    def get_delivered_amount(self, obj):
        if obj.delivered_amount is None:
            return None

        delivered_amount = remove_exponent_from_decimal(obj.delivered_amount)
        return str(delivered_amount)


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
