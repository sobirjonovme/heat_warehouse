from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.warehouse.choices import OrderStatus, ProductType


class ProductUnit(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=127)
    short_name = models.CharField(verbose_name=_("Short name"), max_length=15)

    def __str__(self):
        return self.short_name


class Product(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    unit = models.ForeignKey(ProductUnit, verbose_name=_("Unit"), on_delete=models.SET_NULL, null=True)
    type = models.CharField(verbose_name=_("Type"), max_length=15, choices=ProductType.choices)
    in_stock = models.DecimalField(verbose_name=_("In stock"), max_digits=13, decimal_places=2, default=0)
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)

    def __str__(self):
        return self.name


class Order(BaseModel):
    status = models.CharField(
        verbose_name=_("Status"), max_length=31, choices=OrderStatus.choices, default=OrderStatus.CREATED
    )
    ordered_by = models.ForeignKey(
        to="users.User",
        verbose_name=_("Ordered by"),
        related_name="created_orders",
        on_delete=models.SET_NULL,
        null=True,
    )
    main_stockman = models.ForeignKey(
        to="users.User",
        verbose_name=_("Main stockman"),
        related_name="main_stockman_orders",
        on_delete=models.SET_NULL,
        null=True,
    )
    supplier = models.ForeignKey(
        to="users.User",
        verbose_name=_("Delivered by"),
        related_name="delivered_orders",
        on_delete=models.SET_NULL,
        null=True,
    )
    watchman = models.ForeignKey(
        to="users.User",
        verbose_name=_("Watchman"),
        related_name="watchman_orders",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(BaseModel):
    order = models.ForeignKey(to=Order, verbose_name=_("Order"), related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        to=Product, verbose_name=_("Product"), related_name="order_items", on_delete=models.PROTECT
    )
    needed_amount = models.DecimalField(verbose_name=_("Needed Amount"), max_digits=10, decimal_places=2)
    delivered_amount = models.DecimalField(
        verbose_name=_("Delivered Amount"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    price = models.DecimalField(verbose_name=_("Price"), max_digits=13, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name}"
