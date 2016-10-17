from django.contrib.auth.models import User
from django.shortcuts import render

from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import user_passes_test

from item.models import Item
from users.models import UserProfile


def chef_check(user):
    return user.profile.is_chef


class ChefView(DetailView):
    '''
    Chef page
    '''
    model = User
    template_name = 'chef/cook_page.html'
    slug_field = 'slug'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        profile = UserProfile.objects.get(slug=self.kwargs['slug'])
        chef = User.objects.get(profile=profile)
        return chef

    def get_context_data(self, **kwargs):
        context = super(ChefView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(chef=self.object)
        return context


class IndexView(ListView):
    template_name = 'chef/index.html'
    context_object_name = 'list_users'

    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.order_by('-date_joined').filter(is_superuser=False, profile__is_chef=True)


@user_passes_test(chef_check)
def dashboard(request):
    return render(template_name='chef/dashboard.html', request=request)
