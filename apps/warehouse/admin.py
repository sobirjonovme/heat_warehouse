from django.contrib import admin, messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from unfold import admin as unfold_admin
from unfold.contrib.filters.admin import (RangeDateFilter, RangeDateTimeFilter,
                                          RangeNumericListFilter,
                                          SliderNumericFilter)
from unfold.decorators import action, display

from apps.warehouse.choices import OrderStatus, ProductType
from apps.warehouse.models import Order, OrderItem, Product, ProductUnit


class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 10


class CustomRangeNumericListFilter(RangeNumericListFilter):
    parameter_name = "id"
    title = "items"


@admin.register(ProductUnit)
class ProductUnitAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "name", "short_name")
    list_display_links = ("id", "name", "short_name")
    search_fields = ("id", "name", "short_name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "name", "unit_short_name", "custom_type", "in_stock", "is_active")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("is_active", "type")

    # actions_list = []  # Displayed above the results list
    # actions_row = []  # Displayed in a table row in results list
    actions_detail = ["change_detail_action_activate"]  # Displayed at the top of for in object detail
    # actions_submit_line = []  # Displayed near save in object detail

    readonly_fields = ("created_at", "updated_at")

    @action(description=_("Activate"), url_path="detail-activate")
    def change_detail_action_activate(self, request: HttpRequest, object_id: int):
        """
        Handler for detail action.
        :param request:
        :param object_id: ID of instance that this action was invoked for
        :return: View, as described in section above
        """
        # This is example of action that handled whole logic inside handler
        # function and redirects back to object detail
        product = Product.objects.get(pk=object_id)
        product.is_active = True
        product.save()
        messages.success(request, _("Product was activated."))
        return redirect(reverse_lazy("admin:warehouse_product_change", args=(object_id,)))

    @display(description=_("Unit"), label=True)
    def unit_short_name(self, obj):
        if obj.unit:
            return obj.unit.short_name

    @display(
        description=_("Type"),
        label={
            ProductType.PRIMARY: "info",  # blue
            ProductType.SECONDARY: "warning",  # orange
        },
    )
    def custom_type(self, obj):
        return obj.type

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("unit")
        return qs


class OrderItemInline(unfold_admin.TabularInline):
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
            OrderStatus.CONFIRMED: "info",  # blue
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
        return qs


@admin.register(OrderItem)
class OrderItemAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "order", "product", "needed_amount", "delivered_amount", "price")
    list_display_links = ("id",)
    search_fields = ("id", "order__id", "product__name")
    autocomplete_fields = ("product", "order")
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("product", "order")
        return qs
