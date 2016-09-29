from django.db import models
from item.models import Item
from django.contrib.auth.models import User


class ItemOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)

    def get_total_price(self):
        return self.item.price * self.quantity


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

    customer = models.ForeignKey(User)
    order_date = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(ItemOrder)
    total_price = models.IntegerField(default=0)
    note = models.TextField(default='')
    status = models.CharField(max_length=2,
                              choices=STATUS_CHOICES,
                              default=WAITING)

    def get_total_price(self, status):
        pass




