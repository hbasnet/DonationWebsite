from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^items/(?P<word>.*)/$', views.items_detail, name='items_detail'),
    url(r'^panel/items/list/$', views.items_list, name='items_list'),
    url(r'^panel/items/add/$', views.items_add, name='items_add'),
    url(r'^panel/items/del/(?P<pk>\d+)$', views.items_delete, name='items_delete'),
    url(r'^panel/items/edit/(?P<pk>\d+)$', views.items_edit, name='items_edit'),
]