# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

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

        labels = {
            'name': _(u'Tên sản phẩm'),
            'price': _(u'Giá'),
            'description': _(u'Mô tả sản phẩm'),
            'ingredient': _(u'Thành phần'),
            'in_stock': _(u'Địa chỉ'),
        }


ImageInlineFormSet = inlineformset_factory(Item, Images, fields=('image',), extra=3, max_num=3)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image',)

        labels = {
            'image': _(u'Ảnh')
        }
