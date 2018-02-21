from django.db import models
from django.contrib.auth import get_user_model
from location_field.models.plain import PlainLocationField
from routes.models import Route, Ascent
from routes.scales import convert_scale
# Create your models here.
User = get_user_model()

class Gym(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 200, verbose_name = 'Street, City')
    location = PlainLocationField(based_fields = ['address'], zoom=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.address)

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
    B = 'B'
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
    grade_fr = models.CharField(max_length=20, blank=True, null=True)
    grade_bld_fr = models.CharField(max_length=20, blank=True, null=True)
    ascent_style = models.CharField(max_length = 100, choices = Ascent.ASCENT_STYLE_CHOICES,
                                    verbose_name = 'Style')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.scale == 'YDS' or self.scale == 'FR':
            self.grade = self.grade.lower()
        else:
            self.grade = self.grade.upper()

        if self.route_type=='BLD':
            self.grade_bld_fr = convert_scale(self, 'FR')
        else:
            self.grade_fr = convert_scale(self, 'FR')
        super().save(*args, **kwargs)
