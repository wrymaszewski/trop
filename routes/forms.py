from .models import Route, Place, Ascent
from location_field.forms.plain import PlainLocationField
from location_field.widgets import LocationWidget
from django import forms


class PlaceForm(forms.ModelForm):
    class Meta:
        model=Place
        fields = ('name', 'city', 'country', 'location')
        labels = {
            'city': 'Region'
        }
        def __init__(self, *args, **kwargs):
            super(PlaceForm, self).__init__(*args, **kwargs)
            self.fields['location'].widget = HiddenInput()



class DateInput(forms.DateInput):
    input_type = 'date'

class AscentForm(forms.ModelForm):
    class Meta:
        model = Ascent
        fields = ('route', 'date', 'ascent_style', 'rating', 'description')
        widgets = {
            'date': DateInput(),
        }
