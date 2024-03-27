from django.core.management.base import BaseCommand

from apps.orders.choices import OrderStatus
from apps.orders.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        orders = Order.objects.filter(status=OrderStatus.FINAL_CHECKED)

        for order in orders:
            order.store_items_to_warehouse()
            self.stdout.write(self.style.NOTICE(f"Order {order.id} items stored to warehouse"))

        self.stdout.write(self.style.SUCCESS("Finished"))
