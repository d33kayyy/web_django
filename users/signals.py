import requests
from django.core.files.base import ContentFile
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_logged_in, user_signed_up

from .models import UserProfile


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
        url_image = account_uid[0].get_avatar_url()
        profile[0].name = account_uid[0].extra_data['name']

        # if account_uid[0].provider == 'facebook':
        #
        #     # Update user profile image
        #     new_img = get_img_from_url(url_image)
        #     if new_img != profile[0].avatar:
        #         file_name = account_uid[0].extra_data['id'] + '.jpg'
        #         profile[0].avatar.save(file_name, new_img)

        if account_uid[0].provider == 'google':

            # Update user profile image
            if url_image != profile[0].avatar_link:
                file_name = account_uid[0].extra_data['id'] + '.jpg'
                profile[0].avatar.save(file_name, get_img_from_url(url_image))
                profile[0].avatar_link = url_image

        if account_uid[0].extra_data['gender'] and account_uid[0].extra_data['gender'] == 'male':
            profile[0].gender = 'M'
        else:
            profile[0].gender = 'F'

        profile[0].save()


@receiver(user_signed_up)
def create(**kwargs):
    """
    Create user's profile
    :param kwargs:
    :return:
    """

    user = kwargs['user']

    if not user:
        return

    account_uid = SocialAccount.objects.filter(user_id=user.id)
    profile = UserProfile.objects.create(user=user)

    if account_uid:
        # print(account_uid[0].extra_data)

        if account_uid[0].extra_data['gender'] and account_uid[0].extra_data['gender'] == 'male':
            profile.gender = 'M'
        else:
            profile.gender = 'F'

        # Get user personal information
        profile.name = account_uid[0].extra_data['name']
        profile.email = account_uid[0].extra_data['email']

        # Get user avatar
        url_image = account_uid[0].get_avatar_url()
        file_name = account_uid[0].extra_data['id'] + '.jpg'

        profile.avatar.save(file_name, get_img_from_url(url_image))
        profile.avatar_link = url_image  # for comparison only (to update)

        profile.save()
    else:
        if user:
            profile.name = profile.get_username()
            profile.email = profile.get_email()
            profile.phone = profile.get_phone()

            profile.save()


def get_img_from_url(url):
    return ContentFile(requests.get(url).content)
