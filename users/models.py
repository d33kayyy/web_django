import datetime

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_logged_in, user_signed_up

from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    name = models.CharField(max_length=30, default='users')
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    point = models.PositiveIntegerField(default=0)
    is_chef = models.BooleanField(default=False)
    avatar_link = models.URLField(default='')
    last_update = models.DateTimeField(null=True)

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    def __str__(self):  # Python 2
        return "%s's profile" % self.user.username

    class Meta:
        db_table = 'user_profile'

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


@receiver(user_logged_in)
def populate_user_profile(**kwargs):
    """
    Populate user's profile
    :param kwargs:
    :return:
    """

    user = kwargs['user']

    if not user:
        return

    account_uid = SocialAccount.objects.filter(user_id=user.id)
    profile = UserProfile.objects.get_or_create(user=user)

    if account_uid:
        # Update user display name
        if account_uid[0].provider == 'facebook':
            updated_time = account_uid[0].extra_data['updated_time']
            last_update = datetime.datetime.strptime(updated_time, '%Y-%m-%dT%H:%M:%S+0000')
            last_update = timezone.make_aware(last_update, timezone.get_default_timezone())

            if profile[0].last_update is None or last_update > profile[0].last_update:
                profile[0].last_update = last_update
                profile[0].name = account_uid[0].extra_data['name']

        elif account_uid[0].provider == 'google':
            profile[0].name = account_uid[0].extra_data['name']

        # Update user profile image
        url_image = account_uid[0].get_avatar_url()
        if url_image != profile[0].avatar_link:
            file_name = account_uid[0].extra_data['id'] + '.jpg'
            profile[0].avatar.save(file_name, get_img_from_url(url_image))
            profile[0].avatar_link = url_image

        profile[0].save()


@receiver(user_signed_up)
def create(**kwargs):
    """
    Populate user's profile
    :param kwargs:
    :return:
    """

    user = kwargs['user']

    if not user:
        return

    account_uid = SocialAccount.objects.filter(user_id=user.id)
    profile = UserProfile.objects.create(user=user)

    print(account_uid[0].extra_data)

    if account_uid:

        if account_uid[0].provider == 'facebook':
            updated_time = account_uid[0].extra_data['updated_time']
            last_update = datetime.datetime.strptime(updated_time, '%Y-%m-%dT%H:%M:%S+0000')
            last_update = timezone.make_aware(last_update, timezone.get_default_timezone())

            profile.last_update = last_update

    # Get user personal information
    profile.name = account_uid[0].extra_data['name']
    profile.email = account_uid[0].extra_data['email']

    if account_uid[0].extra_data['gender'] == 'male':
        profile.gender = 'M'
    else:
        profile.gender = 'F'

    # Get user avatar
    url_image = account_uid[0].get_avatar_url()
    file_name = account_uid[0].extra_data['id'] + '.jpg'

    profile.avatar.save(file_name, get_img_from_url(url_image))
    profile.avatar_link = url_image  # for comparison only (to update)

    profile.save()


def get_img_from_url(url):
    return ContentFile(requests.get(url).content)
