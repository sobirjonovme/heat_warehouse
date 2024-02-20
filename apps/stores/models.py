from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


# Create your models here.
class Warehouse(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    stockman = models.ForeignKey(
        to="users.User",
        verbose_name=_("Stockman"),
        related_name="warehouses",
        on_delete=models.SET_NULL,
        null=True,
    )
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)

    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")

    def __str__(self):
        return self.name


class WarehouseProduct(BaseModel):
    warehouse = models.ForeignKey(
        to=Warehouse,
        verbose_name=_("Warehouse"),
        related_name="products",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to="orders.Product",
        verbose_name=_("Product"),
        related_name="warehouses",
        on_delete=models.CASCADE,
    )
    quantity = models.DecimalField(verbose_name=_("Quantity"), max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("Warehouse Product")
        verbose_name_plural = _("Warehouse Products")

    def __str__(self):
        return f"{self.warehouse} - {self.product}"


class WarehouseProductUsage(BaseModel):
    warehouse_product = models.ForeignKey(
        to=WarehouseProduct,
        verbose_name=_("Warehouse product"),
        related_name="usages",
        on_delete=models.CASCADE,
    )
    quantity = models.DecimalField(verbose_name=_("Quantity"), max_digits=15, decimal_places=2)
    to_warehouse = models.ForeignKey(
        to=Warehouse,
        verbose_name=_("To warehouse"),
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    comment = models.TextField(verbose_name=_("Comment"), blank=True, null=True)

    class Meta:
        verbose_name = _("Product Usage")
        verbose_name_plural = _("Product Usages")

    def __str__(self):
        return f"{self.warehouse_product} - {self.quantity}"
