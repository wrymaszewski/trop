from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'(?P<slug>[-\w]+)/new-post/$', views.PostCreateView.as_view(),
    name='new_post'),
    url(r'(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(),
    name='edit_post'),
    url(r'(?P<pk>\d+)/delete/$', views.PostDeleteView.as_view(),
    name='delete_post'),
    url(r'(?P<slug>[-\w]+)/(?P<pk>\d+)/comment/new/$', views.CommentCreateView.as_view(),
    name='new_comment'),
    url(r'(?P<slug>[-\w]+)/(?P<pk>\d+)/comment/edit/$', views.CommentUpdateView.as_view(),
    name='edit_comment'),
    url(r'(?P<slug>[-\w]+)/(?P<pk>\d+)/comment/delete/$', views.CommentDeleteView.as_view(),
    name='delete_comment'),
]
