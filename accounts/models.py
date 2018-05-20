from django.db import models
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse_lazy
from cloudinary.models import CloudinaryField
# Create your models here.

class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return self.username

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length = 100)
    avatar = CloudinaryField('avatar', default = 'user-placeholder-circle_o5pzxf.png',
                null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)

class Group(models.Model):
    name = models.CharField(max_length = 255, unique=True)
    slug = models.SlugField(allow_unicode = True, unique=True)
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('accounts:group_list')

    class Meta:
        ordering = ['name']

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    class Meta:
        unique_together = ('group', 'user')
