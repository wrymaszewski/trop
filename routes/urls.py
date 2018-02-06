from django.conf.urls import url
from . import views

app_name = 'routes'

urlpatterns = [
    url(r'^places/$', views.PlaceList.as_view(),
    name = 'places'),
    url(r'^places/(?P<pk>\d+)/$', views.PlaceDetail.as_view(),
    name = 'place_detail'),
    url(r'^(?P<pk>\d+)/$', views.RouteList.as_view(),
    name = 'route_list'),
    url(r'^ascents/(?P<pk>\d+)/$', views.RouteAscentList.as_view(),
    name = 'route_ascents'),
    url(r'^user/(?P<pk>\d+)/$', views.UserAscentList.as_view(),
    name = 'user_ascents')
]
