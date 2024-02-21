from django.urls import path

from .api_endpoints import debt, order, order_action

app_name = "orders"

urlpatterns = [
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
    # debt
    path("debts/list/", debt.DebtListAPIView.as_view(), name="debts-list"),
    path("debt-payback/<int:order_item_id>/", debt.PaybackDebtAPIView.as_view(), name="debt-payback"),
]
