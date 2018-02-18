from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from accounts.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    group = models.ForeignKey(Group, related_name = 'posts')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering: ['created_at']

class Comment(models.Model):
    post  = models.ForeignKey(Post, related_name = 'comments', on_delete = models.CASCADE)
    author = models.ForeignKey(User, related_name = 'comments', on_delete = models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering: ['created_at']
