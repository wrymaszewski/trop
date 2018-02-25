from django.shortcuts import render, get_object_or_404
from django.views.generic import (CreateView, UpdateView,
                             ListView, DetailView, RedirectView)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from indoor import charts as indoor_charts
from routes import charts as outdoor_charts
from .models import Group, GroupMember, UserProfile
from . import forms
from django.contrib import messages
from posts.models import Post, Comment

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class UserProfileRedirectView(LoginRequiredMixin,RedirectView):
    # redirection to user_profile or new_profile if used did not create one before
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, 'userprofile'):
            return reverse('accounts:user_profile', kwargs = {'username': self.request.user.username})
        else:
            return reverse('accounts:new_profile')

class UserProfileCreationRedirectView(LoginRequiredMixin,RedirectView):
    # redicecting to home of new_profile if user did not create one before
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, 'userprofile'):
            return reverse('home')
        else:
            return reverse('accounts:new_profile')

@login_required
def get_user_profile(request, username):
    # getting user profile based on username
    user = User.objects.select_related().get(username__iexact=username)
    if hasattr(user, 'userprofile'):
        userprofile = user.userprofile
        context_dict = {
                        "userprofile": userprofile,
                        "chart_list": [
                                        indoor_charts.training_line_chart(username),
                                        indoor_charts.gym_pie_chart(username),
                                        outdoor_charts.user_ascent_chart(username),
                                        outdoor_charts.user_ascent_pie_chart(username)
                                        ],
                    }

        return render(request, 'accounts/userprofile_detail.html',
                        context_dict)
    else:
        return render(request, 'accounts/userprofile_error.html', {'username':username})

# CRUD views
class SignUp(CreateView):
    # account creation
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class CreateUserProfile(LoginRequiredMixin, CreateView):
    # profile page creation
    model = UserProfile
    fields = ['first_name', 'last_name', 'email',
                'description', 'avatar', 'hidden']

    def form_valid(self, form):
         self.object = form.save(commit=False)
         self.object.user = self.request.user
         self.success_url = reverse_lazy('accounts:user_profile',
            kwargs={'username': self.object.user.username})

         self.object.save()
         return super().form_valid(form)

class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    # profile page edit
    model = UserProfile
    fields = ['first_name', 'last_name', 'email',
                'description', 'avatar', 'hidden']
    template_name = 'accounts/userprofile_update.html'

    def get_object(self, queryset=None):
        self.object = get_object_or_404(self.model, user=self.request.user)
        self.success_url = reverse_lazy('accounts:user_profile',
            kwargs={'username': self.object.user.username})
        return self.object

###### Groups
class CreateGroup(LoginRequiredMixin, CreateView):
    # creation of new user group
    fields = ('name', 'description')
    model = Group

class SingleGroup(DetailView):
    # view od single user group
    model = Group

class ListGroups(ListView):
    # list of all user groups
    model = Group

class JoinGroup(LoginRequiredMixin, RedirectView):
    # joining existing group
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accounts:group_list')

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        # exception handling if user is alredy a member
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'Warning, already a member!')
        else:
            messages.success(self.request, 'You are now a member!')
        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, RedirectView):
    # leaving user group
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accounts:group_list')

    def get(self, request, *args, **kwargs):
        # exception handling if user is not a member
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you are not in this group!')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group!')
        return super().get(request, *args, **kwargs)
