from typing import Any

from django.contrib import admin, messages
from django.db.models import Model
from django.forms import Form
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from unfold import admin as unfold_admin
from unfold.decorators import action, display

from apps.stores.models import (Product, ProductUnit, Warehouse,
                                WarehouseProduct, WarehouseProductUsage)

from .choices import ProductType


class WarehouseProductInline(unfold_admin.TabularInline):
    model = WarehouseProduct
    extra = 0
    fields = ("id", "warehouse", "product", "quantity")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProductUnit)
class ProductUnitAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "name", "short_name")
    list_display_links = ("id", "name", "short_name")
    search_fields = ("id", "name", "short_name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "name", "unit_short_name", "custom_type", "is_active")
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
        qs = qs.order_by("-id")
        return qs

    def save_model(self, request: HttpRequest, obj: Model, form: Form, change: Any) -> None:
        obj.name = obj.name.lower().capitalize()
        if not obj.created_by:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


@admin.register(Warehouse)
class WarehouseAdmin(unfold_admin.ModelAdmin):
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
