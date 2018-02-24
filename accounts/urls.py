from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'login/$', auth_views.LoginView.as_view(template_name = 'accounts/login.html'),
    name='login'),
    url(r'logout/$', auth_views.LogoutView.as_view(),
    name='logout'),
    url(r'signup/$', views.SignUp.as_view(),
    name='signup'),
    url(r'^$', views.UserList.as_view(),
    name = 'users'),
    url(r'(?P<username>\w+)/profile/$', views.get_user_profile,
    name='user_profile'),
    url(r'redirect/$', views.UserProfileCreationRedirectView.as_view(),
    name='redirect'),
    url(r'redirect-profile/$', views.UserProfileRedirectView.as_view(),
    name='redirect_profile'),
    url(r'new-profile/$', views.CreateUserProfile.as_view(),
    name='new_profile'),
    url(r'(?P<username>\w+)/edit-profile/$', views.UpdateUserProfile.as_view(),
    name='edit_profile'),
    url(r'(?P<username>\w+)/edit-avatar/$', views.ChangeAvatar.as_view(),
    name='edit_avatar'),
    # Groups
    url(r'group/new/$', views.CreateGroup.as_view(),
    name='new_group'),
    url(r'group/(?P<slug>[-\w]+)/$', views.SingleGroup.as_view(),
    name='single_group'),
    url(r'groups/$', views.ListGroups.as_view(),
    name='group_list'),
    url(r'group/(?P<slug>[-\w]+)/join/$', views.JoinGroup.as_view(),
    name='join_group'),
    url(r'group/(?P<slug>[-\w]+)/leave/$', views.LeaveGroup.as_view(),
    name='leave_group')
]
