from django.shortcuts import render
from . import models, forms
from django.views.generic import (CreateView, UpdateView,
    DeleteView, ListView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.

class TrainingList(LoginRequiredMixin, ListView):
    model = models.Training

    def get_queryset(self):
        return models.Training.objects.select_related().filter(user=self.kwargs['pk'])

class TopList(LoginRequiredMixin, ListView):
    model = models.Top

    def get_queryset(self):
        return models.Top.objects.select_related().filter(training=self.kwargs['pk'])

# CRUD operations

class CreateGym(LoginRequiredMixin, CreateView):
    model = models.Gym
    form_class = forms.GymForm
    success_url = reverse_lazy('indoor:new_training')


class CreateTraining(LoginRequiredMixin, CreateView):
    model = models.Training
    form_class = forms.TrainingForm
    success_url = reverse_lazy('indoor:new_top')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class CreateTop(LoginRequiredMixin, CreateView):
    model = models.Top
    form_class = forms.TopForm
    success_url = reverse_lazy('indoor:new_top')
    training = models.Training.objects.latest()

    def get_initial(self):
        return {'training': self.training}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training'] = self.training
        return context


class UpdateTraining(LoginRequiredMixin, UpdateView):
    model = models.Training
    form_class = forms.TrainingForm

    def form_valid(self, form):
        self.object = self.get_object()
        self.success_url = reverse_lazy('indoor:training_list', kwargs = {'pk':self.object.user.pk})
        self.object.save()
        return super().form_valid(form)

class UpdateTop(LoginRequiredMixin, UpdateView):
    model = models.Top
    form_class = forms.TopForm


class DeleteTraining(LoginRequiredMixin, DeleteView):
    model = models.Training

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('indoor:training_list', kwargs = {'pk':self.object.user.pk})
        self.object.delete()
        return HttpResponseRedirect(success_url)

class DeleteTop(LoginRequiredMixin, DeleteView):
    model = models.Top

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('indoor:top_list', kwargs = {'pk':self.object.training.pk})
        self.object.delete()
        return HttpResponseRedirect(success_url)
