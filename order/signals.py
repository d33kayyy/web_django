from django.db.models.signals import post_save
from actstream import action
from .models import Order


def my_handler(sender, instance, created, **kwargs):
    action.send(instance, verb='was created')


post_save.connect(my_handler, sender=Order)
