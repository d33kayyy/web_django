from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import logout
from users import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.cook, name='cook'),
    url(r'^users/', include('users.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', views.profile, name='profile'),
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
