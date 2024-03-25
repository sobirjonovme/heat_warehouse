from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.orders.models import Order, OrderItem


class ItemUpdateSerializer(serializers.Serializer):
    order_item = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all(), required=True)
    delivered_amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=True)
    cash_amount = serializers.DecimalField(max_digits=13, decimal_places=2, min_value=0, required=False)
    card_amount = serializers.DecimalField(max_digits=13, decimal_places=2, min_value=0, required=False)
    debt_amount = serializers.DecimalField(max_digits=13, decimal_places=2, min_value=0, required=False)
    payment_comment = serializers.CharField(required=False)

    class Meta:
        ref_name = "FinalCheckOrderItemUpdateSerializer"


class FinalCheckOrderSerializer(serializers.ModelSerializer):
    items = ItemUpdateSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ("items",)

    def validate(self, attrs):
        order = self.instance

        for item in attrs.get("items"):
            order_item = item.get("order_item")
            if order_item.order != order:
                raise serializers.ValidationError(
                    code="not_belong_to_order", detail={"order_item": _("Order item does not belong to selected order")}
                )

        if len(attrs.get("items")) != order.items.count():
            raise serializers.ValidationError(
                code="not_provided_fully", detail={"items": _("All items of order must be provided")}
            )

        return attrs
