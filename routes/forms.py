from django.forms import ModelForm, DateInput
from .models import Route, Place, Ascent
from location_field.forms.plain import PlainLocationField
from location_field.widgets import LocationWidget


class RouteForm(ModelForm):
    class Meta:
        model = Route
        fields = ('name', 'route_type', 'protection', 'grade', 'scale', 'location')

# class PlaceForm(ModelForm):
#     # location = PlainLocationField(based_fields=['city'],
#     #                                       initial='-22.2876834,-49.1607606')
#     class Meta:
#         model = Place
#         fields = ('name',  'country', 'city', 'location', 'description')
#         # widgets = {
#         # 'location': LocationWidget(based_fields = ['city'], zoom=3)
#         # }

class DateInput(DateInput):
    input_type = 'date'

class AscentForm(ModelForm):
    class Meta:
        model = Ascent
        fields = ('route', 'date', 'ascent_style', 'rating', 'description')
        widgets = {
            'date': DateInput(),
        }
