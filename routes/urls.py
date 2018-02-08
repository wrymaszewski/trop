from django.conf.urls import url
from . import views

app_name = 'routes'

urlpatterns = [
    url(r'^places/$', views.PlaceList.as_view(),
    name = 'places'),
    url(r'^(?P<pk>\d+)/$', views.RouteList.as_view(),
    name = 'route_list'),
    url(r'^route/(?P<pk>\d+)/$', views.RouteAscentList.as_view(),
    name = 'route_ascents'),
    url(r'^user/(?P<pk>\d+)/$', views.UserAscentList.as_view(),
    name = 'user_ascents'),
    url(r'^ascent/new/$', views.CreateAscent.as_view(),
    name = 'new_ascent')
]
