from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductType(models.TextChoices):
    """
    1. Primary - products that are used usually
    2. Secondary - products that are used rarely
    """

    PRIMARY = "primary", _("Primary")
    SECONDARY = "secondary", _("Secondary")
