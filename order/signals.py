from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from .utils import id_generator

from .models import Order


@receiver(models.signals.post_save, sender=Order)
def generate_order_id(sender, instance, created, **kwargs):
    """
    Generate unique ID for the order after it is created
    """
    if not created:
        return
    instance.order_id = id_generator() + str(instance.userprofile_id) + str(instance.pk)
    instance.save()
