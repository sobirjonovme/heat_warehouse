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
