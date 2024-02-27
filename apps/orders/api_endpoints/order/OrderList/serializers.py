from rest_framework import serializers

from apps.orders.choices import OrderStatus
from apps.orders.models import Order
from apps.orders.serializers import UserShortSerializer
from apps.stores.serializers import WarehouseShortSerializer


class OrderListSerializer(serializers.ModelSerializer):
    # total_money = serializers.DecimalField(max_digits=13, decimal_places=2, read_only=True)
    total_money = serializers.SerializerMethodField()
    warehouse = WarehouseShortSerializer(read_only=True)
    ordered_by = UserShortSerializer(read_only=True)
    main_stockman = UserShortSerializer(read_only=True)
    supplier = UserShortSerializer(read_only=True)
    watchman = UserShortSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "total_money",
            "warehouse",
            "ordered_by",
            "main_stockman",
            "supplier",
            "watchman",
            "created_at",
        )

    def get_total_money(self, obj):
        total_money = 0
        if obj.status == OrderStatus.FINAL_CHECKED:
            for item in obj.items.all():
                total_money += item.cash_amount + item.card_amount + item.debt_amount

        return total_money
