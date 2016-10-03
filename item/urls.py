from django.conf.urls import url

from . import views

app_name = 'item'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add/$', views.create_item, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.ItemDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.edit_item, name='edit'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.delete_item, name='delete'),
    # url(r'^(?P<slug>[\w-]+)/review/$', views.CreateReviewView.as_view(), name='add_review'),
]
