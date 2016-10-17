# -*- coding: utf-8 -*-
import os

import itertools
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.utils.text import slugify

# from phonenumber_field.modelfields import PhoneNumberField

numeric = RegexValidator(r'^[+]?\d{9,15}$', message='Số điện thoại không hợp lệ')


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    name = models.CharField(max_length=30, default='users')

    # Customer information
    slug = models.SlugField(unique=True, max_length=100)  # for URL
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True,
                               default=os.path.join(settings.STATIC_URL, "images/default-avatar.png"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, validators=(numeric,), null=True, blank=True)
    allergy = models.TextField(null=True, blank=True, max_length=100)
    point = models.PositiveIntegerField(default=0)

    #  Address information
    address = models.TextField(null=True, blank=True, max_length=100)
    city = models.CharField(max_length=30, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    ward = models.CharField(max_length=30, null=True, blank=True)

    #  For chef
    is_chef = models.BooleanField(default=False)
    info = models.TextField(null=True, blank=True)

    # Extra
    avatar_link = models.URLField(default='')
    last_update = models.DateTimeField(null=True)

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    def __str__(self):  # Python 2
        return "%s's profile" % self.user.username

    class Meta:
        db_table = 'user_profile'

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = orig = slugify(self.get_username())
            print(self.name)

            for x in itertools.count(1):
                if not UserProfile.objects.filter(slug=self.slug).exists():
                    break
                self.slug = "{}-{}".format(orig, x)
        super(UserProfile, self).save(*args, **kwargs)

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def get_username(self):
        if self.user.last_name and self.user.first_name:
            return self.user.last_name + " " + self.user.first_name
        elif self.user.username:
            return self.user.username

    def get_email(self):
        if self.user.email:
            return self.user.email

    def get_phone(self):
        if self.user.phone:
            return self.user.phone

    def get_birthday(self):
        return {'day': self.birthday.day,
                'month': self.birthday.month,
                'year': self.birthday.year}

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# class PhoneModel(models.Model):
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
#                                  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone_number = models.CharField(max_length=16, validators=[phone_regex], blank=True, null=True)  # validators should be a list

# class Address(models.Model):
#     profile = models.ForeignKey(UserProfile, related_name='addresses')
#     city = models.CharField(max_length=30)
#     district = models.CharField(max_length=30)
