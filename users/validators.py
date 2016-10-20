# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

# Validate field with alphabet characters and space only
alphabet = RegexValidator(r'^[a-zA-Z\s]+$', message=_(u'Họ tên không được chứa số và các kí tự đặc biệt'))

# Validate phone number
numeric = RegexValidator(r'^[+]?\d{9,15}$', message=_(u'Số điện thoại không hợp lệ'))
