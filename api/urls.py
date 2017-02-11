from django.conf.urls import url

from . import views

app_name = 'api'

urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^items/$', views.ItemList.as_view(), name='item-list'),
    url(r'^items/(?P<pk>[0-9]+)/$', views.ItemDetail.as_view(), name='item-detail'),

    url(r'^users/$', views.UserList.as_view(), name='users-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='users-detail'),

    url(r'^profile/$', views.UserProfileDetail.as_view(), name='profile'),

    # url(r'^add/$', views.create_item, name='create'),
    # url(r'^(?P<slug>[\w-]+)/$', views.ItemDetailDisplay.as_view(), name='detail'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', views.edit_item, name='edit'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', views.delete_item, name='delete')
]
