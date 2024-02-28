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
        product_name = validated_data.pop("name").lower().capitalize()
        product, _ = Product.objects.get_or_create(name=product_name, defaults=validated_data)
        return product
