from django.views.generic import TemplateView
from chartit import DataPool, Chart
from django.shortcuts import render_to_response
from routes import models
from django.db.models import Count

class Homepage(TemplateView):
    template_name = 'index.html'
