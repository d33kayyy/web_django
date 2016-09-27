from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import UpdateView

from users.models import UserProfile
from .forms import UserProfileForm, SignupForm


# Create your views here.


def cook(request):
    return render(template_name='cook.html', request=request)


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.birthday = form.cleaned_data['birthday']
            profile.gender = form.cleaned_data['gender']
            profile.phone = form.cleaned_data['phone']
            profile.address = form.cleaned_data['address']
            profile.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserProfileForm(instance=request.user.profile)
        if request.user.profile.email:
            form.fields['email'].disabled = True
        # form.fields['point'].disabled = True
        return render(request, 'users/profile.html', {'form': form})


class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = '.'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ChefView(generic.DetailView):
    model = User
    template_name = 'users/profile.html'


class IndexView(generic.ListView):
    template_name = 'users/index.html'
    context_object_name = 'list_users'

    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.order_by('-date_joined').filter(is_superuser=False)


def login_page(request):
    return render(request, 'users/login.html')


def signup_page(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})
