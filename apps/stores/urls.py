from django.urls import path

from .api_endpoints import warehouse_product

app_name = "stores"

urlpatterns = [
    path(
        "warehouse-products/",
        warehouse_product.WarehouseProductListAPIView.as_view(),
        name="warehouse-product-list",
    )
]
