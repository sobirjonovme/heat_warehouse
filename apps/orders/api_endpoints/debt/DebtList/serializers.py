from rest_framework import serializers

from apps.orders.models import OrderItem
from apps.stores.serializers import ProductShortSerializer


class DebtListSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "debt_amount",
            "remain_debt",
            "payment_comment",
        )
