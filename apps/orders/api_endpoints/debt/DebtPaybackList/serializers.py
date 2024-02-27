from rest_framework import serializers

from apps.orders.models import DebtPayback, OrderItem
from apps.orders.serializers import UserShortSerializer
from apps.stores.serializers import ProductShortSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "debt_amount",
            "remain_debt",
            "payment_comment",
        )
        ref_name = "DebtPaybackListOrderItemSerializer"


class DebtPaybackListSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(read_only=True)
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = DebtPayback
        fields = (
            "id",
            "order_item",
            "cash_amount",
            "card_amount",
            "date",
            "user",
        )
