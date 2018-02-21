from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, RedirectView
from django.urls import reverse_lazy, reverse
from . import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from indoor import charts as indoor_charts
from routes import charts as outdoor_charts
from .models import Group, GroupMember
from django.contrib import messages
from posts.models import Post, Comment
# cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api

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
    recent_posts = (Post.objects
                    .filter(group__memberships__in=userprofile.user.user_groups.all())
                    .order_by('created_at')[:5])
    print(recent_posts)
    context_dict = {
                    "userprofile": userprofile,
                    "chart_list": [
                                    indoor_charts.training_line_chart(username),
                                    indoor_charts.gym_pie_chart(username),
                                    outdoor_charts.user_ascent_chart(username),
                                    outdoor_charts.user_ascent_pie_chart(username)
                                    ],
                    'recent_posts': recent_posts
                    }

    return render(request, 'accounts/userprofile_detail.html',
                    context_dict)

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


###### Groups
class CreateGroup(LoginRequiredMixin, CreateView):
    fields = ('name', 'description')
    model = Group

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accounts:single_group', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'Warning, already a member!')
        else:
            messages.success(self.request, 'You are now a member!')
        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accounts:group_list')

    def get(self, request, *args, **kwargs):

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
