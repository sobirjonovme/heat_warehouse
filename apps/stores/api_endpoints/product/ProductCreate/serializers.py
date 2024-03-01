from rest_framework import serializers

from apps.stores.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "unit", "type")
        extra_kwargs = {
            "unit": {"required": True},
        }

    def create(self, validated_data):
        product_name = validated_data.get("name").lower().capitalize()
        unit = validated_data.get("unit")
        product_type = validated_data.get("type")
        product, _ = Product.objects.get_or_create(name=product_name, unit=unit, defaults={"type": product_type})
        return product
