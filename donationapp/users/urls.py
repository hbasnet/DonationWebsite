from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^mylist/$', views.mylist, name='my-list'),
    url(r'^profile/$', views.profile, name='user-profile'),
]