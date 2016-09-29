from django.conf.urls import url

from . import views

app_name = 'item'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.ItemView.as_view(), name='detail'),
    url(r'^add/$', views.CreateItem.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.CreateItem.as_view(), name='create'),
]
