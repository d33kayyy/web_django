import os
import itertools

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse


class Item(models.Model):
    shop = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=100)
    price = models.PositiveIntegerField()
    # image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True)
    ingredient = models.TextField(default='', blank=True)
    description = models.TextField(default='', blank=True)
    in_stock = models.PositiveSmallIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0)

    # category

    def __str__(self):
        return self.name

    def __unicode__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        # return reverse('item.views.ItemView', args=[str(self.id)])
        return reverse('item:detail', kwargs={'slug': self.slug,
                                              # 'pk': self.pk,
                                              })

    def get_ingredient(self):
        '''
        Extract ingredients from the text paragraph
        :return: a list of ingredients
        '''
        ingredient_str = self.ingredient
        ingredients = [line.split(',') for line in ingredient_str.splitlines()]
        return [j.strip() for i in ingredients for j in i if j]

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = orig = slugify(self.name)

            for x in itertools.count(1):
                if not Item.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (orig, x)
                # self.slug = "{}-{}".format(self.pk, slugify(self.name))

        super(Item, self).save(*args, **kwargs)

    def get_primary_image(self):
        '''
        Get the first image as primary
        :return: Image url
        '''
        images = Images.objects.filter(item=self).first()
        return images.image.url

    def get_rating(self):
        '''
        Calculate the rating of the item
        :return: Float number represents the rating
        '''
        from reviews.models import Review
        reviews = Review.objects.filter(item=self)
        if not reviews.count():
            return 0

        total = 0

        for review in reviews:
            total += review.rating

        return float(total / reviews.count())

    def get_rating_int(self):
        return int(self.get_rating() * 20)


class Images(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True)


@receiver(models.signals.post_delete, sender=Images)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes images from filesystem when corresponding Item object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
