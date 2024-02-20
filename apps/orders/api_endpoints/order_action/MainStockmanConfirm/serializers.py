from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User, UserRoles


class OrderConfirmSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(required=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=UserRoles.SUPPLIER), required=False)

    def validate(self, attrs):
        confirm = attrs.get("confirm")
        supplier = attrs.get("supplier")

        # if confirm is True, then supplier must be provided
        if confirm and not supplier:
            raise serializers.ValidationError(code="required", detail={"supplier": _("supplier is required")})

        return attrs
