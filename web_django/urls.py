from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from users import views
from item.views import HomePageView, career, pin

# import notifications.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^career/$', career, name='career'),
    url(r'^pin/$', pin, name='pin'),
    url(r'^users/', include('users.urls')),
    url(r'^item/', include('item.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^reviews/', include('reviews.urls')),
    url(r'^shop/', include('shop.urls')),
    url(r'^notification/', views.notification, name='notification'),
    url(r'^profile/', views.UserProfileUpdate.as_view(), name='profile'),

    # url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^activity/', include('actstream.urls')),

    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
