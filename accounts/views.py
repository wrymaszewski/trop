from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView, RedirectView
from django.urls import reverse_lazy, reverse
from . import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class UserHomeRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, 'userprofile'):
            return '/accounts/users/' + str(self.request.user.userprofile.pk) + '/'
        else:
            return '/accounts/newprofile/'

class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'

    def get_queryset(self):
        return User.objects.all()

class UserProfilePage(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/user_profile.html'

# CRUD views
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class CreateUserProfile(LoginRequiredMixin, CreateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email',
                'description', 'avatar', 'hidden']
    success_url = reverse_lazy('accounts:redirect')

    def form_valid(self, form):
         self.object = form.save(commit=False)
         self.object.user = self.request.user
         self.object.save()
         return super().form_valid(form)

class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email',
                'description', 'avatar', 'hidden']
    template_name = 'accounts/userprofile_update.html'
    success_url = reverse_lazy('accounts:redirect')
