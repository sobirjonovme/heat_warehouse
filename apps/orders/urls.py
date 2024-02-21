from django.urls import path

from ..stores.api_endpoints import product
from .api_endpoints import order, order_action

app_name = "orders"

urlpatterns = [
    # product
    path("products/list/", product.ProductListAPIView.as_view(), name="products-list"),
    path("products/create/", product.ProductCreateAPIView.as_view(), name="product-create"),
    # order
    path("orders/list/", order.OrderListAPIView.as_view(), name="orders-list"),
    path("orders/<int:pk>/detail/", order.OrderDetailAPIView.as_view(), name="order-detail"),
    # order action
    path("orders/create/", order_action.OrderCreateAPIView.as_view(), name="order-create"),
    path(
        "orders/<int:pk>/main-stockman-confirm/",
        order_action.OrderMainStockmanConfirmAPIView.as_view(),
        name="order-main-stockman-confirm",
    ),
    path(
        "orders/<int:pk>/watchman-check/",
        order_action.WatchmanCheckOrderAPIView.as_view(),
        name="order-watchman-check",
    ),
    path(
        "orders/<int:pk>/final-check/",
        order_action.FinalCheckOrderAPIView.as_view(),
        name="order-final-check",
    ),
]
