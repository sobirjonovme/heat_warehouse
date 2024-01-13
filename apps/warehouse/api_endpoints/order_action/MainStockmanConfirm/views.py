from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.warehouse.choices import OrderStatus
from apps.warehouse.models import Order
from apps.warehouse.permissions import CanOrderBeConfirmed

from .serializers import OrderConfirmSerializer


class OrderMainStockmanConfirmAPIView(APIView):
    serializer_class = OrderConfirmSerializer
    permission_classes = (CanOrderBeConfirmed,)

    def get_object(self, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(self.request, order)
        return order

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, pk):
        order = self.get_object(pk)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        confirm = serializer.validated_data.get("confirm")
        supplier = serializer.validated_data.get("supplier")

        if confirm:
            order.status = OrderStatus.CONFIRMED
            order.supplier = supplier
        else:
            order.status = OrderStatus.CANCELED
        order.main_stockman = request.user
        order.save()

        return Response(status=status.HTTP_200_OK)


__all__ = ["OrderMainStockmanConfirmAPIView"]
