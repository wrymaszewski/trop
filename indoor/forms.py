from django import forms
from .models import Top, Training, Gym

class TopForm(forms.ModelForm):
    class Meta:
        model = Top
        fields = ('training', 'route_type', 'ascent_style', 'scale', 'grade', 'description')
        widgets = {'route_type': forms.RadioSelect(),
                    'scale': forms.RadioSelect(),
                    'ascent_style': forms.RadioSelect()}

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ('location', 'date', 'description')
        widgets = {
            'date':forms.DateInput(attrs = {'type': 'date'})
            }

class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ('name', 'address', 'location')
        widgets = {'name': forms.TextInput(attrs = {'placeholder': 'eg. OnSight'}),
                    'address': forms.TextInput(attrs = {'placeholder': 'eg. Obozowa, Warsaw'})}
