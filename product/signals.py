from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import BillingAddress


@receiver(signal=post_save, sender=BillingAddress)
def make_order_submitted(sender, instance, created, **kwargs):
    if created:
        order = instance.order
        order.submitted = True
        order.save()
        return True

    return False
