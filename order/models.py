# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from item.models import Item
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from actstream import action

from users.models import UserProfile


# Create your models here.
class Order(models.Model):
    PROCESSING = 'PR'
    COOKING = 'CO'
    DELIVERING = 'DE'
    FINISHED = 'FI'
    CANCELED = 'CA'
    STATUS_CHOICES = ((PROCESSING, 'Processing'),
                      (COOKING, 'Cooking'),
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
            action.send(self.userprofile, verb=_(u'đã tạo'), action_object=self)
        else:
            super(Order, self).save(*args, **kwargs)
            if self.status == self.PROCESSING:
                return
            elif self.status != self.CANCELED:
                action.send(self, verb=_(u'đã được thay đổi'), action_object=self,
                            target=self.userprofile, status=self.status)
            else:
                action.send(self, verb=_(u'đã bị hủy'), action_object=self, target=self.userprofile)


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
