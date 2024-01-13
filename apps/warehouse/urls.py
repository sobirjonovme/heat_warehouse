from django.urls import path

from .api_endpoints import order, order_action, product

app_name = "warehouse"

urlpatterns = [
    # product
    path("products/list/", product.ProductListAPIView.as_view(), name="products-list"),
    path("products/create/", product.ProductCreateAPIView.as_view(), name="product-create"),
    # order
    path("orders/list/", order.OrderListAPIView.as_view(), name="orders-list"),
    # order action
    path("orders/create/", order_action.OrderCreateAPIView.as_view(), name="order-create"),
    path(
        "orders/<int:pk>/main-stockman-confirm/",
        order_action.OrderMainStockmanConfirmAPIView.as_view(),
        name="order-main-stockman-confirm",
    ),
]
