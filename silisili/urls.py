from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from users import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.cook, name='cook'),
    url(r'^users/', include('users.urls')),
    url(r'^item/', include('item.urls')),

    url(r'^accounts/profile/', views.UserProfileUpdate.as_view(), name='profile'),
    url(r'^accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
