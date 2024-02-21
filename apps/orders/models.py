from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.orders.choices import OrderStatus


class Order(BaseModel):
    status = models.CharField(
        verbose_name=_("Status"), max_length=31, choices=OrderStatus.choices, default=OrderStatus.CREATED
    )
    warehouse = models.ForeignKey(
        to="stores.Warehouse",
        verbose_name=_("Warehouse"),
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
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
        verbose_name=_("Supplier"),
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

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(BaseModel):
    order = models.ForeignKey(to=Order, verbose_name=_("Order"), related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        to="stores.Product", verbose_name=_("Product"), related_name="order_items", on_delete=models.PROTECT
    )
    needed_amount = models.DecimalField(verbose_name=_("Needed Amount"), max_digits=15, decimal_places=2)
    delivered_amount = models.DecimalField(
        verbose_name=_("Delivered Amount"), max_digits=15, decimal_places=2, null=True, blank=True
    )

    image = models.ImageField(verbose_name=_("Image"), upload_to="order_items/", null=True, blank=True)
    comment = models.TextField(verbose_name=_("Comment"), null=True, blank=True)

    cash_amount = models.DecimalField(verbose_name=_("Cash Amount"), max_digits=13, decimal_places=2, default=0)
    card_amount = models.DecimalField(verbose_name=_("Card Amount"), max_digits=13, decimal_places=2, default=0)
    debt_amount = models.DecimalField(verbose_name=_("Debt Amount"), max_digits=13, decimal_places=2, default=0)
    remain_debt = models.DecimalField(verbose_name=_("Remain Debt"), max_digits=13, decimal_places=2, default=0)
    payment_comment = models.TextField(verbose_name=_("Payment Comment"), null=True, blank=True)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name}"


class DebtPayback(BaseModel):
    order_item = models.ForeignKey(
        to=OrderItem, verbose_name=_("Order Item"), related_name="debt_paybacks", on_delete=models.CASCADE
    )
    cash_amount = models.DecimalField(verbose_name=_("Amount"), max_digits=13, decimal_places=2, default=0)
    card_amount = models.DecimalField(verbose_name=_("Amount"), max_digits=13, decimal_places=2, default=0)
    date = models.DateField(verbose_name=_("Date"))
    user = models.ForeignKey(
        to="users.User", verbose_name=_("User"), related_name="debt_paybacks", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = _("Debt Payback")
        verbose_name_plural = _("Debt Paybacks")

    def __str__(self):
        return f"Debt Payback #{self.id} - {self.order_item}"
