from django import forms

from .models import Item, Images


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'price',
            # 'image',
            'description',
            'in_stock'
        ]


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image',)
