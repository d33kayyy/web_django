# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile, numeric

BIRTH_YEAR_CHOICES = [x for x in range(1960, 2016, 1)]


class SignupForm(forms.Form):
    alphabet = RegexValidator(r'^[a-zA-Z\s]+$', message=_(u'Họ tên không được chứa số và các kí tự đặc biệt'))

    last_name = forms.CharField(max_length=30, label=_(u'Họ'), validators=(alphabet,))
    first_name = forms.CharField(max_length=30, label=_(u'Tên'), validators=(alphabet,))
    phone = forms.CharField(label=_(u"Điện thoại"), validators=(numeric,))
    email = forms.EmailField(label=_(u"Email"))
    password1 = forms.CharField(max_length=16, label=_(u"Mật khẩu"), widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=16, label=_(u"Nhập lại mật khẩu"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'phone', 'email', 'password1', 'password2']

        widgets = {
            'password1': forms.PasswordInput,
            'password2': forms.PasswordInput
        }
        labels = {
            'password1': _(u"Mật khẩu"),
            'password2': _(u"Nhập lại mật khẩu"),
            'email': _(u"Email")
        }

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password2']
        if user.password:
            user.set_password(user.password)
        else:
            user.set_unusable_password()
        user.save()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2


# DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class DateInput(forms.DateInput):
    input_type = 'date'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthday', 'gender', 'email', 'phone', 'address', 'allergy', 'city', 'district', 'ward']
        widgets = {
            # 'gender': forms.Select,
            # 'birthday': DateInput(),
            'birthday': forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
            'address': forms.Textarea(attrs={'rows': 1}),
            # 'point': forms.TextInput,
            'allergy': forms.Textarea(attrs={'rows': 1})
        }
        labels = {
            # 'name': _('Họ và tên'),
            'birthday': _(u'Ngày sinh'),
            'gender': _(u'Giới tính'),
            'phone': _(u'Số điện thoại'),
            'address': _(u'Địa chỉ'),
            'allergy': _(u'Tiền sử dị ứng'),
            'city': _(u'Tỉnh/Thành Phố'),
            'district': _(u'Quận/Huyện'),
            'ward': _(u'Phường/Xã')
            # 'point': _('Điểm tích lũy'),
        }

    email = forms.CharField(disabled=True)
