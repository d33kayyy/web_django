from django.conf.urls import url

from . import views

app_name = 'shop'

urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^(?P<slug>[\w-]+)/$', views.ShopView.as_view(), name='detail'),
]
