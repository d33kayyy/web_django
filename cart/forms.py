from django import forms

from django.utils.translation import ugettext_lazy as _


class ItemOrderForm(forms.Form):
    item_id = forms.IntegerField()
    quantity = forms.IntegerField(min_value=0)


class ItemForm(forms.Form):
    item_id = forms.IntegerField()


class InformationForm(forms.Form):
    name = forms.CharField(max_length=30, label=_(u'Tên người nhận'))
    email = forms.EmailField(label=_('Email'))
    phone = forms.CharField(max_length=16, label=_(u'Số điện thoại'))
    address = forms.CharField(max_length=250, label=_(u'Địa chỉ'))
    city = forms.CharField(max_length=30, label=_(u'Tỉnh/Thành Phố'))
    district = forms.CharField(max_length=30, label=_(u'Quận/Huyện'))
    note = forms.CharField(max_length=250, label=_(u'Ghi chú'), required=False)