from django.urls import path

from .api_endpoints import order_actions, product

app_name = "warehouse"

urlpatterns = [
    # products
    path("products/list/", product.ProductListAPIView.as_view(), name="products-list"),
    path("products/create/", product.ProductCreateAPIView.as_view(), name="product-create"),
    # orders
    # order actions
    path("orders/create/", order_actions.OrderCreateAPIView.as_view(), name="order-create"),
    path(
        "orders/<int:pk>/main-stockman-confirm/",
        order_actions.OrderMainStockmanConfirmAPIView.as_view(),
        name="order-main-stockman-confirm",
    ),
]
