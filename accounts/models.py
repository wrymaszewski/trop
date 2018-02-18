from django.db import models
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.urlresolvers import reverse_lazy



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

class Group(models.Model):
    name = models.CharField(max_length = 255, unique=True)
    slug = models.SlugField(allow_unicode = True, unique=True)
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('accounts:group_list')

    class Meta:
        ordering = ['name']



class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships')
    user = models.ForeignKey(User, related_name='user_groups')
    def __str__(self):
        return self.user.username
    class Meta:
        unique_together = ('group', 'user')
