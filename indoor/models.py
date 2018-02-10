from django.db import models
from django.contrib.auth import get_user_model
from location_field.models.plain import PlainLocationField
from routes.models import Route, Ascent
# Create your models here.
User = get_user_model()

class Gym(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 200)
    location = PlainLocationField(based_fields = ['city'], zoom=10)

    def __str__(self):
        return self.name

class Training(models.Model):
    user = models.ForeignKey(User, related_name='trainings',
        on_delete=models.CASCADE)
    location = models.ForeignKey(Gym,
        related_name='trainings', on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.location.name + ' - ' + self.date

class Top(models.Model):

    training = models.ForeignKey(Training,
        related_name='tops', on_delete=models.CASCADE)
    route_type = models.CharField(max_length = 100, choices = Route.ROUTE_TYPE_CHOICES)
    scale = models.CharField(max_length = 100, choices = Route.SCALE_CHOICES, default = Route.FR)
    grade = models.CharField(max_length=10)
    ascent_style = models.CharField(max_length = 100, choices = Ascent.ASCENT_STYLE_CHOICES)
