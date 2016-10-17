from django.conf.urls import url

from . import views

app_name = 'chef'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^(?P<slug>[\w-]+)/$', views.ChefView.as_view(), name='detail'),

]
