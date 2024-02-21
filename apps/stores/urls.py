from django.urls import path

from .api_endpoints import product, warehouse_product

app_name = "stores"

urlpatterns = [
    # product
    path("products/list/", product.ProductListAPIView.as_view(), name="products-list"),
    path("products/create/", product.ProductCreateAPIView.as_view(), name="product-create"),
    # warehouse product
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
