from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, RedirectView
from django.urls import reverse_lazy, reverse
from . import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.
class UserProfileRedirectView(LoginRequiredMixin,RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, 'userprofile'):
            return reverse_lazy('accounts:user_profile',
                                kwargs = {'username':self.request.user.username})
        else:
            return reverse('accounts:new_profile')

class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'

    def get_queryset(self):
        return User.objects.all()

@login_required
def get_user_profile(request, username):
    userprofile = UserProfile.objects.select_related().get(user__username__iexact = username)
    return render(request, 'accounts/userprofile_detail.html',
                    {"userprofile": userprofile})

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

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)
