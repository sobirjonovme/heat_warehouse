from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.choices import OrderStatus
from apps.orders.models import Order
from apps.orders.permissions import CanOrderBeFinalChecked

from .serializers import FinalCheckOrderSerializer


class FinalCheckOrderAPIView(APIView):
    serializer_class = FinalCheckOrderSerializer
    permission_classes = (CanOrderBeFinalChecked,)

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
            order_item.cash_amount = item.get("cash_amount", 0)
            order_item.card_amount = item.get("card_amount", 0)
            order_item.debt_amount = item.get("debt_amount", 0)
            order_item.save()

        order.status = OrderStatus.FINAL_CHECKED
        order.main_stockman = request.user
        order.save()

        return Response(status=status.HTTP_200_OK)


__all__ = ["FinalCheckOrderAPIView"]
