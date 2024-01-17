from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserRoles(models.TextChoices):
    ADMIN = "admin", _("Admin")
    # for warehouse
    MAIN_STOCKMAN = "main_stockman", _("Main Stockman")
    STOCKMAN = "stockman", _("Stockman")
    SUPPLIER = "supplier", _("Supplier")
    WATCHMAN = "watchman", _("Watchman")


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.ADMIN,
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
