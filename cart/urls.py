from django.conf.urls import url

from . import views

app_name = 'cart'

urlpatterns = [
    url(r'^$', views.CartView.as_view(), name='cart'),
    url(r'^add/$', views.AddItemToCart.as_view(), name='add'),
    url(r'^remove/$', views.RemoveItemFromCart.as_view(), name='remove'),
    url(r'^info/$', views.information, name='info'),
    url(r'^confirm/$', views.confirmation, name='confirm'),
]
