# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, ListView
from django.utils.translation import ugettext_lazy as _

from item.models import Item
from users.models import UserProfile


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
        # get all items created by this chef
        context['items'] = Item.objects.filter(chef=self.object)
        return context


class IndexView(ListView):
    template_name = 'chef/index.html'
    context_object_name = 'list_users'

    def get_queryset(self):
        """Return the list of chefs."""
        return User.objects.order_by('-date_joined').filter(is_superuser=False, profile__is_chef=True)


class SuperOrManagerPermissionsMixin(AccessMixin):
    """
    Super class for permission checking
    Check if the logged in user is a chef or not
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return self.handle_no_permission()
        if self.user_has_permissions():
            return super(SuperOrManagerPermissionsMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def user_has_permissions(self):
        profile = UserProfile.objects.get(user=self.request.user)
        return profile.is_chef


class DashboardView(SuperOrManagerPermissionsMixin, DetailView):
    """
    Chef page
    """
    model = User
    template_name = 'chef/dashboard.html'
    context_object_name = 'user'
    permission_denied_message = _(u'Bạn không có quyền truy cập trang này')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(chef=self.object)
        return context
