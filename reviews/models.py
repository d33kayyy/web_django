from django.db import models
from django.dispatch import receiver

from item.models import Item
from users.models import UserProfile


# Create your models here.

class Review(models.Model):
    MAX_STARS = 5
    RATING_STARS = (
        (1, 'One star'),
        (2, 'Two stars'),
        (3, 'Three stars'),
        (4, 'Four stars'),
        (5, 'Five stars'),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(UserProfile)
    content = models.TextField(blank=True, default='')
    rating = models.IntegerField(choices=RATING_STARS, default=4)
    updated_time = models.DateTimeField(auto_now=True)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        unique_together = (("item", "reviewer"),)

    def __str__(self):
        return self.content

    def __unicode__(self):
        return "{}".format(self.content)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_rating(self):
        return range(self.rating)


@receiver(models.signals.post_save, sender=Review)
def update_item_rating(sender, instance, **kwargs):
    """
    Update the rating of item reviewed
    """
    item = instance.item
    item.rating = item.get_rating()
    item.save()
