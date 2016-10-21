from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["userprofile", "total_price", "status"]
