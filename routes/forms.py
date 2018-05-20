from .models import Ascent, Sector, Route
from django import forms


class AscentForm(forms.ModelForm):
    class Meta:
        model = Ascent
        fields = ('route', 'date', 'ascent_style', 'rating', 'description')
        widgets = {'date': forms.DateInput(
                            attrs={'class': 'datepicker', 'type': 'date'}),
                   'ascent_style': forms.RadioSelect(),
                   'rating': forms.RadioSelect()}


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ('name', 'region', 'location')
        widgets = {'name': forms.TextInput(
                            attrs={'placeholder': 'eg. El Capitan'}),
                   'region': forms.TextInput(
                            attrs={'placeholder': 'eg. Yosemite, USA'})}


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['sector', 'name', 'route_type',
                  'protection', 'scale', 'grade']
        widgets = {'route_type': forms.RadioSelect(),
                   'protection': forms.RadioSelect(),
                   'scale': forms.RadioSelect(),
                   'name': forms.TextInput(
                               attrs={"placeholder": "eg. The Nose"})}
