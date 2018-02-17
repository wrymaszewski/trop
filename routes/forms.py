from .models import Ascent, Place
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class AscentForm(forms.ModelForm):
    class Meta:
        model = Ascent
        fields = ('route', 'date', 'ascent_style', 'rating', 'description')
        widgets = {'date': DateInput()}

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'country', 'city', 'location')
