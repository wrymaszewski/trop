from django.forms import ModelForm
from .models import Route, Place, Ascent

class RouteForm(ModelForm):
    class Meta:
        model = Route
        fields = ('name', 'route_type', 'protection', 'grade', 'scale', 'location')

class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'city', 'country', 'description')

class AscentForm(ModelForm):
    class Meta:
        model = Ascent
        fields = ('date', 'route', 'ascent_style', 'description')
