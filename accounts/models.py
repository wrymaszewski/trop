from django.db import models
from django.contrib import auth
from django.contrib.auth import get_user_model


# Create your models here.

class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return self.username

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length = 100, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True,
    upload_to='accounts/avatars/', default = 'accounts/avatars/user_placeholder.png')
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
