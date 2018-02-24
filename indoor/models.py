from django.db import models
from django.contrib.auth import get_user_model
from location_field.models.plain import PlainLocationField
from routes.models import Route, Ascent
from routes.scales import convert_scale
from django.core.validators import RegexValidator
# Create your models here.
User = get_user_model()

class Gym(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 200, verbose_name = 'Street, City',
                                validators = [RegexValidator(
                                regex='.+,\s.+',
                                message = 'Input needs to consist of street and city names divided by a comma (,) and a space'
                                )])
    location = PlainLocationField(based_fields = ['address'], zoom=10,
                                    default='52.2479423,20.953566')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.address)

    def save(self, *args, **kwargs):
        self.address = self.address.title()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        get_latest_by = 'created_at'



class Training(models.Model):
    user = models.ForeignKey(User, related_name='trainings',
        on_delete=models.CASCADE)
    location = models.ForeignKey(Gym, verbose_name = 'Gym',
        related_name='trainings', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location.name + ' : ' + str(self.date)

    class Meta:
        ordering = ['date']
        get_latest_by = 'created_at'

class Top(models.Model):
    B = 'BLD'
    R = 'R'
    ROUTE_TYPE_CHOICES = (
        (B, 'Boulder'),
        (R, 'Rope')
    )


    training = models.ForeignKey(Training,
        related_name='tops', on_delete=models.CASCADE)
    route_type = models.CharField(max_length = 100, choices = ROUTE_TYPE_CHOICES, default=R,
                                    verbose_name = 'Type')
    scale = models.CharField(max_length = 100, choices = Route.SCALE_CHOICES, default = Route.FR)
    grade = models.CharField(max_length=20)
    grade_converted = models.CharField(max_length=20, blank=True, null=True)
    ascent_style = models.CharField(max_length = 100, choices = Ascent.ASCENT_STYLE_CHOICES,
                                    verbose_name = 'Style', default = Ascent.OS)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.scale == 'YDS' or self.scale == 'FR':
            self.grade = self.grade.lower()
        else:
            self.grade = self.grade.upper()
        if self.route_type=='BLD':
            self.grade_converted = convert_scale(self, 'V')
        else:
            self.grade_converted = convert_scale(self, 'FR')
        # error handling
        if not type(self.grade_converted) is str:
            self.grade_converted = self.grade
        super().save(*args, **kwargs)
