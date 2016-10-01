from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Item(models.Model):
    chef = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chef')
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    # image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True)
    ingredient = models.TextField(default='', blank=True)
    description = models.TextField(default='', blank=True)
    in_stock = models.PositiveSmallIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # category
    # review

    def __str__(self):
        return self.name

    def __unicode__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        # return reverse('item.views.ItemView', args=[str(self.id)])
        return "/item/{}".format(self.id)


class Images(models.Model):
    item = models.ForeignKey(Item, related_name='images')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True)
