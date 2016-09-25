from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import UpdateView

from users.models import UserProfile
from .forms import UserProfileForm


# Create your views here.


def cook(request):
    return render(template_name='cook.html', request=request)


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # post = form.save(commit=False)
            # post.
            return HttpResponseRedirect()
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form': form})


# class UserProfileUpdate(UpdateView):
#     model = UserProfile
#     fields = ['name', 'birthday', 'gender', 'email', 'phone', 'address', 'point']
#     widgets = {
#         'gender': forms.Select,
#         'birthday': forms.SelectDateWidget,
#     }


def user_page(request):
    pass


class ChefView(generic.DetailView):
    model = User
    template_name = 'profile.html'


class IndexView(generic.ListView):
    template_name = 'users/index.html'
    context_object_name = 'list_users'

    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.order_by('-date_joined').filter(is_superuser=False)
