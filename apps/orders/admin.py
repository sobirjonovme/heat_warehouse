from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold import admin as unfold_admin
from unfold.contrib.filters.admin import (RangeNumericListFilter,
                                          SliderNumericFilter)
from unfold.decorators import display

from apps.orders.choices import OrderStatus
from apps.orders.models import DebtPayback, Order, OrderItem


class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 10


class CustomRangeNumericListFilter(RangeNumericListFilter):
    parameter_name = "id"
    title = "items"


class OrderItemInline(unfold_admin.StackedInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(unfold_admin.ModelAdmin):
    list_display = [
        "id",
        "show_status_customized_color",
        "ordered_by",
        "main_stockman",
        "supplier",
        "watchman",
        "warehouse",
    ]

    list_display_links = ("id", "show_status_customized_color")
    search_fields = (
        "id",
        "status",
        "ordered_by__username",
        "ordered_by__first_name",
        "ordered_by__last_name",
        "supplier__username",
        "supplier__first_name",
        "supplier__last_name",
        "main_stockman__username",
        "main_stockman__first_name",
        "main_stockman__last_name",
        "watchman__username",
        "watchman__first_name",
        "watchman__last_name",
    )
    list_filter = (
        "warehouse",
        "status",
        # ("created_at", RangeDateFilter),  # Date range search, __gte and __lte lookup
    )
    # Display submit button in filters
    list_filter_submit = True

    inlines = (OrderItemInline,)
    readonly_fields = ("created_at", "updated_at")

    @display(
        description=_("Status"),
        ordering="status",
        label={
            OrderStatus.CREATED: "info",  # blue
            OrderStatus.CONFIRMED: "warning",  # blue
            OrderStatus.DELIVERED: "warning",  # orange
            OrderStatus.FINAL_CHECKED: "success",  # green
            OrderStatus.CANCELED: "danger",  # red
        },
    )
    def show_status_customized_color(self, obj):
        return obj.status

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related(
            "ordered_by",
            "main_stockman",
            "supplier",
            "watchman",
        )
        qs = qs.order_by("-id")
        return qs


@admin.register(OrderItem)
class OrderItemAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "order", "product", "needed_amount", "delivered_amount", "total_money", "warehouse_")
    list_display_links = ("id", "order", "product")
    search_fields = ("id", "order__id", "product__name")
    list_filter = ("order__warehouse",)
    autocomplete_fields = ("product", "order")
    readonly_fields = ("created_at", "updated_at")

    @display(description=_("Total money"))
    def total_money(self, obj):
        total_money = obj.cash_amount + obj.card_amount + obj.debt_amount
        # format total_money like 1,000.00
        return "{:,.2f}".format(total_money)

    @display(description=_("Warehouse"))
    def warehouse_(self, obj):
        return obj.order.warehouse

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("product", "order", "order__warehouse")
        return qs


@admin.register(DebtPayback)
class DebtPaybackAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "order_item", "cash_amount", "card_amount", "date")
    list_display_links = ("id", "order_item")
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("order_item")
        return qs
