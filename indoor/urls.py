from django.conf.urls import url
from . import views

app_name = 'indoor'

urlpatterns = [
    url(r'top/new/$', views.CreateTop.as_view(),
    name = 'new_top'),
    url(r'top/update/(?P<pk>\d+)/$', views.UpdateTop.as_view(),
    name = 'edit_top'),
    url(r'top/delete/(?P<pk>\d+)/$', views.DeleteTop.as_view(),
    name = 'delete_top'),
    url(r'training/new/$', views.CreateTraining.as_view(),
    name = 'new_training'),
    url(r'training/update/(?P<pk>\d+)/$', views.UpdateTraining.as_view(),
    name = 'edit_training'),
    url(r'training/delete/(?P<pk>\d+)/$', views.DeleteTraining.as_view(),
    name = 'delete_training'),
    url(r'gym/new/$', views.CreateGym.as_view(),
    name = 'new_gym'),
    url(r'training/(?P<pk>\d+)/$', views.TopList.as_view(),
    name = 'top_list'),
    url(r'(?P<username>\w+)/trainings/$', views.TrainingList.as_view(),
    name = 'training_list')
]
