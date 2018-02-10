from django.shortcuts import render
from . import models, forms
from django.views.generic import (CreateView, UpdateView,
    DeleteView, ListView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# class TrainingList(ListView):
#     model = models.Training
#
# class TrainingDetail(DetailView):
#     model = models.Training

# CRUD operations

class CreateGym(LoginRequiredMixin, CreateView):
    model = models.Gym
    form_class = forms.GymForm

class CreateTraining(LoginRequiredMixin, CreateView):
    model = models.Training
    form_class = forms.TrainingForm

class CreateTop(LoginRequiredMixin, CreateView):
    model = models.Top
    form_class = forms.TopForm

class UpdateTraining(LoginRequiredMixin, UpdateView):
    model = models.Training
    form_class = forms.TrainingForm

class UpdateTop(LoginRequiredMixin, UpdateView):
    model = models.Top
    form_class = forms.TopForm

class DeleteTraining(LoginRequiredMixin, DeleteView):
    model = models.Training

class DeleteTop(LoginRequiredMixin, DeleteView):
    model = models.Top
