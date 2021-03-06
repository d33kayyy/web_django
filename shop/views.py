from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, ListView
from django.utils.translation import ugettext_lazy as _

from item.models import Item
from users.models import UserProfile


class ShopView(DetailView):
    '''
    shop page
    '''
    model = User
    template_name = 'shop/shop_page.html'
    slug_field = 'slug'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        profile = UserProfile.objects.get(slug=self.kwargs['slug'])
        shop = User.objects.get(profile=profile)
        return shop

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        # get all items created by this shop
        context['items'] = Item.objects.filter(shop=self.object)
        return context


class IndexView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'list_users'

    def get_queryset(self):
        """Return the list of shops."""
        return User.objects.order_by('-date_joined').filter(is_superuser=False, profile__is_shop=True)


class SuperOrManagerPermissionsMixin(AccessMixin):
    """
    Super class for permission checking
    Check if the logged in user is a shop or not
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return self.handle_no_permission()
        if self.user_has_permissions():
            return super(SuperOrManagerPermissionsMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def user_has_permissions(self):
        profile = UserProfile.objects.get(user=self.request.user)
        return profile.is_shop


class DashboardView(SuperOrManagerPermissionsMixin, DetailView):
    """
    shop page
    """
    model = User
    template_name = 'shop/dashboard.html'
    context_object_name = 'user'
    permission_denied_message = _(u'''You don't have access to this page''')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(shop=self.object)
        return context
