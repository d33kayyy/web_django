from django.db import models

from item.models import Item
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from actstream import action
from notifications.signals import notify

from users.models import UserProfile


# Create your models here.
class Order(models.Model):
    PROCESSING = 'PR'
    DELIVERING = 'DE'
    FINISHED = 'FI'
    CANCELED = 'CA'
    STATUS_CHOICES = ((PROCESSING, 'Processing'),
                      (DELIVERING, 'Delivering'),
                      (FINISHED, 'Finished'),
                      (CANCELED, 'Canceled'),)

    userprofile = models.ForeignKey(UserProfile, related_name='orders', null=True)
    order_id = models.CharField(max_length=30, null=True, blank=True)
    receiver = models.CharField(max_length=30, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)
    shipping = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=2,
                              choices=STATUS_CHOICES,
                              default=PROCESSING)

    # Customer information, could be different from the user's profile
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    note = models.TextField(default='', null=True, blank=True)
    city = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    ward = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    def __unicode__(self):
        return "{}".format(str(self.pk))

    def get_total_price(self):
        '''
        Get the total price of the order
        :return:
        '''
        total_price = 0
        items = self.items.all()
        if items:
            for item in items:
                total_price += item.get_subtotal()

        self.total_price = total_price

        return total_price

    def save(self, *args, **kwargs):
        if not self.id:
            super(Order, self).save(*args, **kwargs)
            action.send(self.userprofile, verb=_(u'is created'), action_object=self)

        else:
            super(Order, self).save(*args, **kwargs)

            status = dict(self.STATUS_CHOICES).get(self.status)

            if self.status == self.PROCESSING:  # Default status, no change
                return
            elif self.status == self.CANCELED:  # Message when order is canceled
                action.send(self, verb=_(u'is canceled'), action_object=self, target=self.userprofile)
                # notify.send(self, verb=_(u'is canceled'), action_object=self, recipient=self.userprofile.user,
                #             order_id=self.order_id)
            else:  # Message when status change
                action.send(self, verb=_(u'is changed'), action_object=self, target=self.userprofile, status=status)
                # notify.send(self, verb=_(u'is changed'), action_object=self, recipient=self.userprofile.user,
                #             status=status, order_id=self.order_id)


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item)
    quantity = models.PositiveSmallIntegerField(default=0)
    is_reviewed = models.BooleanField(default=False)

    def get_subtotal(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.item.name

    def __unicode__(self):
        return "{}".format(self.item.name)
