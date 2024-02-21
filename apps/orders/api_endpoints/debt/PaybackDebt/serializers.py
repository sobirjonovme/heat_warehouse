from rest_framework import serializers

from apps.orders.models import DebtPayback


class PaybackDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtPayback
        fields = (
            "id",
            "cash_amount",
            "card_amount",
            "date",
        )

    def create(self, validated_data):
        instance = super().create(validated_data)

        order_item = instance.order_item
        total_payback = instance.cash_amount + instance.card_amount
        order_item.remain_debt -= total_payback
        order_item.cash_amount += instance.cash_amount
        order_item.card_amount += instance.card_amount
        order_item.save()

        return instance
