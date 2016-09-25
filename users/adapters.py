from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import UserProfile


class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user

        # if user:
        #     profile = UserProfile.objects.get_or_create(user=user)
        #
        #     if sociallogin.account.provider == 'facebook':
        #         url_image = sociallogin.account.get_avatar_url()
        #         file_name = sociallogin.account.extra_data['id'] + '.jpg'
        #         profile.avatar.save(file_name, get_img_from_url(url_image))
        #
        #     elif sociallogin.account.provider == 'google':
        #         pass
        #
        #     profile.save()
        # else:
        #     return
