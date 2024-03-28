from django.template import loader
from django.utils import dateformat, timezone
from django.utils.translation import activate

from apps.common.models import TelegramNotification
from apps.common.services.common import remove_exponent_from_decimal
from apps.common.services.telegram import send_telegram_message

__all__ = ["send_order_notification"]


def send_order_notification(order):
    activate("uz")
    tg_notification = TelegramNotification.get_solo()

    if tg_notification.is_enabled:
        order_items = []
        items_qs = order.items.all().select_related("product", "product__unit")
        for item in items_qs:
            order_items.append(
                {
                    "product": item.product.name,
                    "needed_amount": str(remove_exponent_from_decimal(item.needed_amount)),
                    "unit": item.product.unit.short_name,
                    "comment": f"\n{item.comment}" if item.comment else "",
                }
            )

        supplier_tg_id = order.supplier.telegram_id

        context = {
            "order": order,
            "supplier": order.supplier.get_full_name(),
            "supplier_tg_id": supplier_tg_id,
            "time": dateformat.format(order.created_at.astimezone(timezone.get_current_timezone()), "j-F H:i"),
            "stockman": order.ordered_by.get_full_name(),
            "warehouse": order.warehouse.name,
            "order_items": order_items,
        }

        msg_text = loader.render_to_string("bot/order_notification.html", context)
        send_telegram_message(tg_notification.bot_token, tg_notification.chat_id, msg_text)
