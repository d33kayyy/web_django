from django import forms
from django.utils.translation import ugettext_lazy as _


class ItemOrderForm(forms.Form):
    """
    Form for items in order (cart page)
    """
    item_id = forms.IntegerField()
    quantity = forms.IntegerField(min_value=0)


class ItemForm(forms.Form):
    """
    Form for item deletion (cart page)
    """
    item_id = forms.IntegerField()


class InformationForm(forms.Form):
    """
    Form for information page
    """
    name = forms.CharField(max_length=30, label=_('Receiver'))
    email = forms.EmailField(label=_('Email'))
    phone = forms.CharField(max_length=16, label=_('Phone number'))
    address = forms.CharField(max_length=250, label=_('Address'))
    city = forms.CharField(max_length=30, label=_('City'))
    district = forms.CharField(max_length=30, label=_('District'))
    ward = forms.CharField(max_length=30, label=_('Ward'), required=False)
    note = forms.CharField(max_length=250, label=_('Note'), required=False)