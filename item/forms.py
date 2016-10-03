from django import forms
from django.forms import inlineformset_factory

from .models import Item, Images


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'price',
            # 'image',
            'description',
            'ingredient',
            'in_stock'
        ]
        help_texts = {
            'ingredient': "Separate by commas or new line"
        }


ImageInlineFormSet = inlineformset_factory(Item, Images, fields=('image',), extra=3, max_num=3)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image',)
