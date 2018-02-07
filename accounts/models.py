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
    avatar = models.ImageField()
    email = models.EmailField(),
    description = models.TextField()
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
