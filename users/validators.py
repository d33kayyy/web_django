from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

# Validate field with alphabet characters and space only
alphabet = RegexValidator(r'^[a-zA-Z\s]+$', message=_('Name cannot contain number or special characters'))

# Validate phone number
numeric = RegexValidator(r'^[+]?\d{9,15}$', message=_('Invalid phone number'))
