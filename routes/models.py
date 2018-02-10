from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100, verbose_name = 'Region')
    country = models.CharField(max_length = 100)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.city, self.country)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.city = self.city.capitalize()
        lat = self.location.split(',')[0]
        lng = self.location.split(',')[1]
        self.country = self.country.capitalize()
        super().save(*args, **kwargs)

    class Meta:
        get_latest_by = 'created_at'
        ordering = ['country', 'city', 'name']

class Route(models.Model):

        # Route types
        SP = 'SP'
        MP = 'MP'
        BLD = 'BLD'
        ROUTE_TYPE_CHOICES = ((SP,'Single-Pitch'),
                             (MP,'Multi-Pitch'),
                             (BLD,'Boulder'))

        # Scales
        YDS = 'YDS'
        FR = 'FR'
        UIAA = 'UIAA'
        POL = 'POL'
        V = 'V'
        SCALE_CHOICES = ((YDS,'YDS'),
                        (FR,'French'),
                        (UIAA,'UIAA'),
                        (POL,'Polish'),
                        (V,'Verm'))

        # Protection
        EQ = 'EQ'
        TR = 'TR'
        MX = 'MX'
        PROTECTION_CHOICES = ((EQ,'Equipped'),
                            (TR,'TRAD'),
                            (MX,'Mixed'))

        name = models.CharField(max_length = 100)
        route_type = models.CharField(max_length = 50, choices = ROUTE_TYPE_CHOICES, default = SP)
        protection = models.CharField(max_length = 100, choices = PROTECTION_CHOICES, default = EQ)
        scale = models.CharField(max_length = 100, choices = SCALE_CHOICES, default = FR)
        grade = models.CharField(max_length = 20)
        location = models.ForeignKey(Place ,related_name='routes', verbose_name = 'Crag', on_delete = models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def save(self, *args, **kwargs):
            self.name = self.name.capitalize()
            if self.scale == 'YDS' or self.scale == 'FR':
                self.grade = self.grade.lower()
            else:
                self.grade = self.grade.upper()
            super().save(*args, **kwargs)

        def __str__(self):
            return "{} ({}, {}, {})".format(self.name, self.location.name,
            self.location.city, self.location.country)

        class Meta:
            ordering = ['location', 'name']
            get_latest_by = 'created_at'


class Ascent(models.Model):

    # Ascent styles
    OS = 'OS'
    FL = 'FL'
    RP = 'RP'
    PP = 'PP'
    AF = 'AF'
    TR = 'TR'
    ASCENT_STYLE_CHOICES = ((OS,'OS'),
                            (FL,'Flash'),
                            (RP,'RP'),
                            (PP,'PP'),
                            (AF,'AF'),
                            (TR,'TR'))

    # Ratings
    UNRATED = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    RATING_CHOICES = ((UNRATED,'No rating'),
                    (LOW, 'Low'),
                    (MEDIUM, 'Medium'),
                    (HIGH, 'High'))

    route = models.ForeignKey(Route, related_name='ascents', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ascents', on_delete=models.CASCADE)
    date = models.DateField()
    ascent_style = models.CharField(max_length = 20, choices = ASCENT_STYLE_CHOICES)
    rating = models.IntegerField(choices = RATING_CHOICES, default=UNRATED)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' : ' + self.route.name

    class Meta:
        ordering = ['date']
        get_latest_by = ['created_at']
