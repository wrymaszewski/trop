from django import forms
from .models import Top, Training, Gym

class DateInput(forms.DateInput):
    input_type = 'date'

class TopForm(forms.ModelForm):
    class Meta:
        model = Top
        fields = ('training', 'route_type', 'scale', 'grade', 'ascent_style')

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ('location', 'date', 'description')
        widgets = {
            'date':DateInput()
        }

class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ('name', 'address', 'location')