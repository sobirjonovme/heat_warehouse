from rest_framework import serializers

from apps.orders.models import Order
from apps.orders.serializers import OrderUserSerializer


class OrderListSerializer(serializers.ModelSerializer):
    total_money = serializers.DecimalField(max_digits=13, decimal_places=2, read_only=True)
    ordered_by = OrderUserSerializer(read_only=True)
    main_stockman = OrderUserSerializer(read_only=True)
    supplier = OrderUserSerializer(read_only=True)
    watchman = OrderUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "total_money",
            "ordered_by",
            "main_stockman",
            "supplier",
            "watchman",
            "created_at",
        )
