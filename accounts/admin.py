from django.contrib import admin
from .models import UserProfile, Group, GroupMember

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Group)
admin.site.register(GroupMember)
