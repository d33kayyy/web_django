from django import forms


class ItemOrderForm(forms.Form):
    item_id = forms.IntegerField()
    quantity = forms.IntegerField(min_value=0)

class ItemForm(forms.Form):
    item_id = forms.IntegerField()