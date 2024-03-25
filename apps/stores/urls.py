from django.urls import path

from .api_endpoints import product, warehouse, warehouse_product

app_name = "stores"

urlpatterns = [
    # warehouse
    path("list/", warehouse.WarehouseListAPIView.as_view(), name="warehouses-list"),
    # product
    path("product-units/", product.ProductUnitListAPIView.as_view(), name="product-units-list"),
    path("products/list/", product.ProductListAPIView.as_view(), name="products-list"),
    path("products/create/", product.ProductCreateAPIView.as_view(), name="product-create"),
    path("products/outgoings/", product.ProductOutgoingsListAPIView.as_view(), name="product-outgoings"),
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
