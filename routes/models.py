from django.db import models
from django.utils.text import slugify
from location_field.models.plain import PlainLocationField
from django.core.validators import RegexValidator
from .scales import convert_scale

from django.contrib.auth import get_user_model
User = get_user_model()


class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(allow_unicode=True)
    subregion = models.CharField(max_length=100, unique=False)
    region = models.CharField(max_length=250, verbose_name='Region, Country',
                              validators=[RegexValidator(
                                          regex='.+,\s.+',
                                          message='Input needs to consist\
                                            of region and country names\
                                            divided by a comma (,) and a space'
                                          )])
    country = models.CharField(max_length=100)
    location = PlainLocationField(based_fields=['region'], zoom=7,
                                  default='37.6564706,-119.5724832')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.name = self.name.title()
        self.country = self.region.split(', ')[1].title()
        self.region = self.region.split(', ')[0].title()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.region, self.country)

    class Meta:
        get_latest_by = 'created_at'
        ordering = ['country', 'region', 'name']


class Route(models.Model):

        # Route types
        SP = 'SP'
        MP = 'MP'
        BLD = 'BLD'
        ROUTE_TYPE_CHOICES = ((SP, 'Single-Pitch'),
                              (MP, 'Multi-Pitch'),
                              (BLD, 'Boulder'))

        # Scales
        YDS = 'YDS'
        FR = 'FR'
        UIAA = 'UIAA'
        POL = 'POL'
        V = 'V'
        SCALE_CHOICES = ((YDS, 'YDS'),
                         (FR, 'French'),
                         (UIAA, 'UIAA'),
                         (POL, 'Polish'),
                         (V, 'Vermin'))

        # Protection
        EQ = 'EQ'
        TR = 'TR'
        MX = 'MX'
        PROTECTION_CHOICES = ((EQ, 'Equipped'),
                              (TR, 'TRAD'),
                              (MX, 'Mixed'))

        name = models.CharField(max_length=100)
        slug = models.SlugField(allow_unicode=True)
        route_type = models.CharField(max_length=50,
                                      choices=ROUTE_TYPE_CHOICES,
                                      default=SP, verbose_name='Type')
        protection = models.CharField(max_length=100,
                                      choices=PROTECTION_CHOICES,
                                      default=EQ)
        scale = models.CharField(max_length=50,
                                 choices=SCALE_CHOICES,
                                 default=FR)
        grade = models.CharField(max_length=20, null=True, blank=True)
        grade_converted = models.CharField(max_length=20, null=True,
                                           blank=True)
        sector = models.ForeignKey(Sector, related_name='routes',
                                   on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            self.name = self.name.title()

            if self.scale == 'YDS' or self.scale == 'FR':
                self.grade = self.grade.lower()
            else:
                self.grade = self.grade.upper()
            if self.route_type == 'BLD':
                self.grade_converted = convert_scale(self, 'V')
            else:
                self.grade_converted = convert_scale(self, 'FR')
            # error handling
            if not type(self.grade_converted) is str:
                self.grade_converted = self.grade
            super().save(*args, **kwargs)

        def __str__(self):
            return "{} ({}, {}, {})".format(self.name,
                                            self.sector.name,
                                            self.sector.region,
                                            self.sector.country)

        class Meta:
            ordering = ['sector', 'name']
            get_latest_by = 'created_at'


class Ascent(models.Model):

    # Ascent styles
    OS = 'OS'
    FL = 'FL'
    RP = 'RP'
    PP = 'PP'
    AF = 'AF'
    TR = 'TR'
    UF = 'UF'
    ASCENT_STYLE_CHOICES = ((OS, 'Onsight'),
                            (FL, 'Flash'),
                            (RP, 'Red point'),
                            (PP, 'Pink point'),
                            (AF, 'All free'),
                            (TR, 'Top rope'),
                            (UF, 'Unfinished'))

    # Ratings
    UNRATED = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    RATING_CHOICES = ((UNRATED, 'No rating'),
                      (LOW, 'Low'),
                      (MEDIUM, 'Medium'),
                      (HIGH, 'High'))

    route = models.ForeignKey(Route, related_name='ascents',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ascents',
                             on_delete=models.CASCADE)
    date = models.DateField()
    ascent_style = models.CharField(max_length=20,
                                    choices=ASCENT_STYLE_CHOICES,
                                    default=OS, verbose_name='Style')
    rating = models.IntegerField(choices=RATING_CHOICES, default=UNRATED)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' : ' + self.route.name

    class Meta:
        ordering = ['date']
        get_latest_by = ['created_at']
