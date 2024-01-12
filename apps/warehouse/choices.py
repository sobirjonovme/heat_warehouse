from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductType(models.TextChoices):
    """
    1. Primary - products that are used usually
    2. Secondary - products that are used rarely
    """

    PRIMARY = "primary", _("Primary")
    SECONDARY = "secondary", _("Secondary")


class OrderStatus(models.TextChoices):
    """
    1. stockman creates order
    2. Main stockman confirms order and send it to supplier
    3. Supplier brings order to the warehouse and watchman confirms it
    4. Main stockman checks order and confirms it
    """

    CREATED = "created", _("Created")
    CONFIRMED = "confirmed", _("Confirmed")
    DELIVERED = "delivered", _("Delivered")
    FINAL_CHECKED = "final_checked", _("Final checked")
