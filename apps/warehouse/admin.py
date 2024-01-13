from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.warehouse.models import Order, OrderItem, Product, ProductUnit


@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_name")
    list_display_links = ("id", "name", "short_name")
    search_fields = ("id", "name", "short_name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "unit_short_name", "type", "in_stock", "is_active")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("unit", "is_active")

    def unit_short_name(self, obj):
        if obj.unit:
            return obj.unit.short_name

    unit_short_name.short_description = _("Unit")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("unit")
        return qs


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "ordered_by",
        "main_stockman",
        "supplier",
        "watchman",
    )
    list_display_links = ("id", "status")
    search_fields = (
        "id",
        "status",
        "ordered_by__first_name",
        "ordered_by__last_name",
        "supplier_by__first_name",
        "supplier_by__last_name",
        "main_stockman__first_name",
        "main_stockman__last_name",
        "watchman__first_name",
        "watchman__last_name",
    )
    list_filter = ("status",)
    inlines = (OrderItemInline,)

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
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "needed_amount", "delivered_amount", "price")
    list_display_links = ("id",)
    search_fields = ("id", "order__id", "product__name")
    list_filter = ("product", "order")
    autocomplete_fields = ("product", "order")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("product", "order")
        return qs
