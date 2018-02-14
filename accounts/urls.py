from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'login/$', auth_views.LoginView.as_view(template_name = 'accounts/login.html'), name='login'),
    url(r'logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^$', views.UserList.as_view(), name = 'users'),
    url(r'(?P<username>\w+)/profile/$', views.get_user_profile, name='user_profile'),
    url(r'redirect/$', views.UserProfileRedirectView.as_view(), name='redirect'),
    url(r'^new-profile/$', views.CreateUserProfile.as_view(), name='new_profile'),
    url(r'(?P<username>\w+)/edit-profile/$', views.UpdateUserProfile.as_view(), name='edit_profile')
]
