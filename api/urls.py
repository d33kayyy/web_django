from django.conf.urls import url

from . import views

app_name = 'api'

# Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'items', views.ItemViewSet)
# router.register(r'users', views.UserViewSet)
# router.register(r'shops', views.ShopViewSet)

urlpatterns = [
    url(r'^$', views.api_root, name='root'),
    # url(r'^', include(router.urls)),

    url(r'^items/$', views.ItemList.as_view(), name='item-list'),
    url(r'^items/(?P<pk>[0-9]+)/$', views.ItemDetail.as_view(), name='item-detail'),

    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    url(r'^profile/$', views.UserProfileDetail.as_view(), name='profile'),

    url(r'^shops/$', views.ShopList.as_view(), name='shop-list'),
    url(r'^shops/(?P<pk>[0-9]+)/$', views.ShopDetail.as_view(), name='shop-detail'),

    # url(r'^reviews/(?P<pk>[0-9]+)/$', views.ReviewDetail.as_view(), name='review-detail'),
    url(r'^reviews/$', views.ReviewCreateView.as_view(), name='review-create'),

    url(r'^orders/$', views.OrderListView.as_view(), name='order-list'),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetailView.as_view(), name='order-detail'),
]
