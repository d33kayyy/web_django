from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserProfile


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Voornaam')
    last_name = forms.CharField(max_length=30, label='Achternaam')

    class Meta:
        model = User

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'birthday', 'gender', 'email', 'phone', 'address', 'point']
        widgets = {
            'gender': forms.Select,
            'birthday': forms.SelectDateWidget,
        }
        disabled = {}

