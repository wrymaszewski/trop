from django.conf.urls import url
from . import views

app_name = 'routes'

urlpatterns = [
    url(r'^regions/$', views.SectorList.as_view(),
        name='sectors'),
    url(r'^(?P<slug>[-\w]+)/$', views.RouteList.as_view(),
        name='route_list'),
    url(r'^(?P<sector_slug>[-\w]+)/(?P<route_slug>[-\w]+)/ascents/$',
        views.RouteAscentList.as_view(), name='route_ascents'),
    url(r'^(?P<username>\w+)/ascents/$', views.UserAscentList.as_view(),
        name='user_ascents'),
    url(r'^ascent/new/$', views.CreateAscent.as_view(),
        name='new_ascent'),
    url(r'^(?P<sector_slug>[-\w]+)/(?P<route_slug>[-\w]+)/ascent/new/$',
        views.CreateAscentFromRoute.as_view(), name='new_ascent_from_route'),
    url(r'^ascent/(?P<pk>\d+)/delete/$', views.DeleteAscent.as_view(),
        name='delete_ascent'),
    url(r'^ascent/(?P<pk>\d+)/edit/$', views.UpdateAscent.as_view(),
        name='update_ascent'),
    url(r'^ascent-route/new/$', views.CreateRoute.as_view(),
        name='new_route'),
    url(r'^route/(?P<slug>[-\w]+)/new/$',
        views.CreateRouteFromSector.as_view(), name='new_route_from_sector'),
    url(r'^ascent-sector/new/$', views.CreateSector.as_view(),
        name='new_sector'),
    url(r'^sector/new/$', views.CreateSectorRedirect.as_view(),
        name='new_sector_redirect'),
    url(r'^route/new/$', views.CreateRouteRedirect.as_view(),
        name='new_route_redirect')
]
