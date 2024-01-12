from django.urls import path

from .api_endpoints import product

app_name = "warehouse"

urlpatterns = [
    path("products/list/", product.ProductListAPIView.as_view(), name="product-list"),
    # orders
    # order actions
]
