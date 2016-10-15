from django.conf.urls import url

from . import views

app_name = 'reviews'

urlpatterns = [
    url(r'^$', views.ReviewPageView.as_view(), name='index'),
    url(r'^create/$', views.ItemReview.as_view(), name='create'),
]
