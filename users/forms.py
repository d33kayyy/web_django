from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile

BIRTH_YEAR_CHOICES = [x for x in range(1900, 2016, 1)]


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    class Meta:
        model = User

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [ 'birthday', 'gender', 'email', 'phone', 'address']
        widgets = {
            # 'gender': forms.Select,
            'birthday': forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
            # 'point': forms.TextInput,
        }
        labels = {
            # 'name': _('Họ và tên'),
            'birthday': _('Ngày sinh'),
            'gender': _('Giới tính'),
            'phone': _('Số điện thoại'),
            'address': _('Địa chỉ'),
            # 'point': _('Điểm tích lũy'),
        }

    email = forms.CharField(disabled=True)

