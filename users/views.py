# -*- coding: utf-8 -*-
from actstream.models import actor_stream, any_stream
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views import generic
from django.utils.translation import ugettext_lazy as _

from order.models import Order
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


@login_required
def notification(request):
    actions = any_stream(request.user.profile)
    return render(request, 'notification.html', {'actions': actions})
