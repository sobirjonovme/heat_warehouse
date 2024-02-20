from django.contrib import admin
from unfold import admin as unfold_admin

from apps.stores.models import (Warehouse, WarehouseProduct,
                                WarehouseProductUsage)


class WarehouseProductInline(unfold_admin.TabularInline):
    model = WarehouseProduct
    extra = 0
    fields = ("id", "warehouse", "product", "quantity")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Warehouse)
class ProductUnitAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "name", "stockman", "is_active")
    list_display_links = (
        "id",
        "name",
    )
    search_fields = (
        "id",
        "name",
    )
    readonly_fields = ("created_at", "updated_at")
    inlines = (WarehouseProductInline,)


@admin.register(WarehouseProductUsage)
class WarehouseProductUsageAdmin(unfold_admin.ModelAdmin):
    list_display = (
        "id",
        "warehouse_product",
        "quantity",
    )
    list_display_links = (
        "id",
        "warehouse_product",
    )
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("to_warehouse",)
