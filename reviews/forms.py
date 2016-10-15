from django.forms import ModelForm
from django import forms

from order.models import ItemOrder
from .models import Review


class ReviewForm(ModelForm):
    item_order_id = forms.IntegerField()

    class Meta:
        model = Review
        fields = ('item', 'rating', 'content', 'item_order_id')

    def save(self, commit=True):
        item_order_id = self.cleaned_data['item_order_id']
        item_order = ItemOrder.objects.get(pk=item_order_id)
        item_order.is_reviewed = True
        item_order.save()

        return super(ReviewForm, self).save(commit=commit)

