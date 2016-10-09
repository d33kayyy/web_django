from django.conf.urls import url

from . import views

app_name = 'order'

urlpatterns = [
    url(r'^$', views.CartView.as_view(), name='cart'),
    url(r'^add/$', views.AddItemToCart.as_view(), name='add'),
    url(r'^remove/$', views.RemoveItemFromCart.as_view(), name='remove'),
    url(r'^info/$', views.information, name='info'),
    url(r'^confirm/$', views.confirmation, name='confirm'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.OrderView.as_view(), name='detail'),
    # url(r'^update/$', views.UpdateItemInCart.as_view(), name='update'),
]
