from django.urls import path

from .api_endpoints import warehouse_product

app_name = "stores"

urlpatterns = [
    path(
        "warehouse-products/",
        warehouse_product.WarehouseProductListAPIView.as_view(),
        name="warehouse-product-list",
    ),
    path(
        "warehouse-products/<int:pk>/use/",
        warehouse_product.UseWarehouseProductAPIView.as_view(),
        name="warehouse-product-use",
    ),
]
