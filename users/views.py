from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.utils.translation import ugettext_lazy as _

from item.models import Item
from users.models import UserProfile
from .forms import UserProfileForm


class UserProfileUpdate(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    '''
    User profile page: /accounts/profile
    '''
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = '.'
    success_message = _(u'Thay đổi đã được lưu lại.')

    def get_object(self, queryset=None):
        return self.request.user.profile


class ChefView(generic.DetailView):
    '''
    Chef page
    '''
    model = User
    template_name = 'users/detail.html'
    slug_field = 'slug'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        profile = UserProfile.objects.get(slug=self.kwargs['slug'])
        return User.objects.get(profile=profile)

    def get_context_data(self, **kwargs):
        context = super(ChefView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(chef=self.object)
        return context


class IndexView(generic.ListView):
    template_name = 'users/index.html'
    context_object_name = 'list_users'

    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.order_by('-date_joined').filter(is_superuser=False)
