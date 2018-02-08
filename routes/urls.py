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
    name = 'new_ascent'),
    url(r'^ascent/delete/(?P<pk>\d+)/$', views.DeleteAscent.as_view(),
    name='delete_ascent'),
    url(r'^ascent/update/(?P<pk>\d+)/$', views.UpdateAscent.as_view(),
    name='update_ascent'),
    url(r'^new/$', views.CreateRoute.as_view(),
    name='new_route'),
    url(r'^place/new/$', views.CreatePlace.as_view(),
    name='new_place')

]
