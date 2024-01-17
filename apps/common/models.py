from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class VersionHistory(BaseModel):
    version = models.CharField(_("Version"), max_length=64)
    required = models.BooleanField(_("Required"), default=True)

    class Meta:
        verbose_name = _("Version history")
        verbose_name_plural = _("Version histories")

    def __str__(self):
        return self.version


class FrontendTranslation(BaseModel):
    key = models.CharField(_("Key"), max_length=255, unique=True)
    text = models.CharField(_("Text"), max_length=1024)

    class Meta:
        verbose_name = _("Frontend translation")
        verbose_name_plural = _("Frontend translations")

    def __str__(self):
        return str(self.key)


class TelegramNotification(SingletonModel, BaseModel):
    bot_token = models.CharField(_("Bot token"), max_length=255)
    chat_id = models.CharField(_("Chat ID"), max_length=255)
    is_enabled = models.BooleanField(_("Is enabled"), default=False)

    class Meta:
        verbose_name = _("Telegram notification")
        verbose_name_plural = _("Telegram notification")

    def __str__(self):
        return str(_("Telegram notification"))
