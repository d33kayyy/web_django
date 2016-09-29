from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    chef = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True)
    description = models.TextField()
    in_stock = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # category
    # review

    def __str__(self):
        return self.name
