from django.conf.urls import url

from . import views

app_name = 'item'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.ItemDetailView.as_view(), name='detail'),
    url(r'^add/$', views.create_item, name='create'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.edit_item, name='edit'),
]
