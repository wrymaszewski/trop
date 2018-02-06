from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.core.urlresolvers import reverse_lazy
from . import forms
from .models import User
from django.contrib.auth.models import User

# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class UserList(ListView):
    model = User
    template_name = 'accounts/user_list.html'

    def get_queryset(self):
        return User.objects.all()
