from django.conf.urls import url

from . import views

app_name = 'order'

urlpatterns = [
    url(r'^$', views.ListOrdersView.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.OrderDetailView.as_view(), name='detail'),
    # url(r'^update/$', views.UpdateItemInCart.as_view(), name='update'),
]
