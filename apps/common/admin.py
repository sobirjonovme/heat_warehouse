from django.contrib import admin
from solo.admin import SingletonModelAdmin
from unfold import admin as unfold_admin

from apps.common.models import FrontendTranslation, TelegramNotification, VersionHistory


@admin.register(VersionHistory)
class VersionHistoryAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "version", "required", "created_at", "updated_at")
    list_display_links = ("id", "version")
    list_filter = ("required", "created_at", "updated_at")
    search_fields = ("version",)


@admin.register(FrontendTranslation)
class FrontTranslationAdmin(unfold_admin.ModelAdmin):
    list_display = ("id", "key", "text", "created_at", "updated_at")
    list_display_links = ("id", "key")
    list_filter = ("created_at", "updated_at")
    search_fields = ("key", "version")


@admin.register(TelegramNotification)
class TelegramNotificationAdmin(unfold_admin.ModelAdmin, SingletonModelAdmin):
    readonly_fields = ("created_at", "updated_at")
