from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from unfold import admin as unfold_admin
from unfold.decorators import display
from unfold.forms import (AdminPasswordChangeForm, UserChangeForm,
                          UserCreationForm)

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, unfold_admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ("id", "username", "first_name", "last_name", "custom_role")
    list_display_links = ("id", "username", "first_name", "last_name")
    search_fields = ("id", "username", "first_name", "last_name")
    list_filter = ("role", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "role")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "role", "username", "password1", "password2"),
            },
        ),
    )

    @display(description=_("Role"), ordering="role", label=True)
    def custom_role(self, obj):
        return obj.get_role_display()
