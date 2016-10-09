from django.db import models
from item.models import Item
from django.contrib.auth.models import User

from users.models import UserProfile


# Create your models here.
class Order(models.Model):
    WAITING = 'WA'
    COOKING = 'CO'
    DELIVERING = 'DE'
    FINISH = 'FI'
    CANCEL = 'CA'
    STATUS_CHOICES = ((WAITING, 'Waiting'),
                      (COOKING, 'Cooking'),
                      (DELIVERING, 'Delivering'),
                      (FINISH, 'Finished'),
                      (CANCEL, 'Canceled'),)

    customer = models.ForeignKey(UserProfile, related_name='orders', null=True)
    receiver = models.CharField(max_length=30, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)
    note = models.TextField(default='')
    status = models.CharField(max_length=2,
                              choices=STATUS_CHOICES,
                              default=WAITING)
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=100)
    # email = models.EmailField()
    city = models.CharField(max_length=30)
    district = models.CharField(max_length=30)

    def get_total_price(self):
        total_price = 0
        items = self.items.all()
        if items:
            for item in items:
                total_price += item.get_subtotal()

        self.total_price = total_price

        return total_price


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item)
    quantity = models.PositiveSmallIntegerField(default=0)

    def get_subtotal(self):
        return self.item.price * self.quantity
