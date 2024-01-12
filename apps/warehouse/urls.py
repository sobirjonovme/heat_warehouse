from django.urls import path

from .api_endpoints import product

app_name = "warehouse"

urlpatterns = [
    # products
    path("products/list/", product.ProductListAPIView.as_view(), name="products-list"),
    path("products/create/", product.ProductCreateAPIView.as_view(), name="product-create"),
    # orders
    # order actions
]
