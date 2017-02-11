from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import Item, Images


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'description', 'ingredient', 'in_stock']
        help_texts = {
            'ingredient': _("Separate by commas or new line")
        }

        labels = {
            'name': _('Product name'),
            'price': _('Price'),
            'description': _('Description'),
            'ingredient': _('Ingredients'),
            'in_stock': _('Stock'),
        }


# Set of image forms for an item
ImageInlineFormSet = inlineformset_factory(Item, Images, fields=('image',), extra=3, max_num=3)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image',)
        labels = {
            'image': _('Image')
        }
