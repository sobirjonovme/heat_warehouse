from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.choices import OrderStatus
from apps.orders.models import Order
from apps.orders.permissions import CanOrderBeChecked

from .serializers import WatchmanCheckOrderSerializer


class WatchmanCheckOrderAPIView(APIView):
    serializer_class = WatchmanCheckOrderSerializer
    permission_classes = (CanOrderBeChecked,)

    def get_object(self, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(self.request, order)
        return order

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, pk):
        order = self.get_object(pk)
        serializer = self.serializer_class(instance=order, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        for item in serializer.validated_data.get("items"):
            order_item = item.get("order_item")
            delivered_amount = item.get("delivered_amount")
            order_item.delivered_amount = delivered_amount
            order_item.save()

        order.status = OrderStatus.DELIVERED
        order.watchman = request.user
        order.save()

        return Response(status=status.HTTP_200_OK)


__all__ = ["WatchmanCheckOrderAPIView"]
