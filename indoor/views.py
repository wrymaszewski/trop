from . import models, forms, charts
from django.views.generic import (CreateView, UpdateView,
                        DeleteView, ListView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.

class TrainingList(LoginRequiredMixin, ListView):
    model = models.Training

    def get_queryset(self):
        queryset = super().get_queryset()
        self.username = self.kwargs.get('username')
        return queryset.filter(user__username__iexact = self.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chart_list'] = [charts.gym_pie_chart(self.username),
                                charts.training_line_chart(self.username)]
        context['username'] = self.username
        return context

class TopList(LoginRequiredMixin, ListView):
    model = models.Top
    template_name = 'indoor/top_list.html'

    def get_queryset(self):
        self.training = models.Training.objects.select_related().get(pk=self.kwargs.get('pk'))
        self.tops = self.training.tops.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['top_list'] = self.tops
        context['lat'] = self.training.location.location.split(',')[0]
        context['lng'] = self.training.location.location.split(',')[1]
        context['training'] = self.training
        context['chart_list'] = [
                                charts.training_grade_pie_chart(self.kwargs.get('pk')),
                                charts.training_style_pie_chart(self.kwargs.get('pk'))
                                ]
        return context

# CRUD operations
class CreateGym(LoginRequiredMixin, CreateView):
    model = models.Gym
    form_class = forms.GymForm
    success_url = reverse_lazy('indoor:new_training')


class CreateTraining(LoginRequiredMixin, CreateView):
    model = models.Training
    form_class = forms.TrainingForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        self.success_url = reverse_lazy('indoor:new_top', kwargs={'pk': self.object.pk})
        return super().form_valid(form)

class CreateTop(LoginRequiredMixin, CreateView):
    model = models.Top
    form_class = forms.TopForm

    def get_initial(self):
        return {'training': models.Training.objects.get(pk=self.kwargs.get('pk'))}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training'] = models.Training.objects.get(pk = self.kwargs.get('pk'))
        return context

    def form_valid(self,form):
        self.success_url = reverse_lazy('indoor:new_top', kwargs = {'pk': self.kwargs.get('pk')})
        return super().form_valid(form)

class UpdateTraining(LoginRequiredMixin, UpdateView):
    model = models.Training
    form_class = forms.TrainingForm
    template_name = 'indoor/training_update.html'

    def form_valid(self, form):
        self.object = self.get_object()
        self.success_url = reverse_lazy('indoor:training_list', kwargs = {'username':self.object.user.username})
        self.object.save()
        return super().form_valid(form)

class UpdateTop(LoginRequiredMixin, UpdateView):
    model = models.Top
    form_class = forms.TopForm
    template_name = 'indoor/top_update.html'

    def form_valid(self,form):
        self.object = self.get_object()
        self.success_url = reverse_lazy('indoor:top_list', kwargs ={'pk':self.object.training.pk})
        self.object.save()
        return super().form_valid(form)

class DeleteTraining(LoginRequiredMixin, DeleteView):
    model = models.Training

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('indoor:training_list', kwargs = {'username':self.object.user.username})
        self.object.delete()
        return HttpResponseRedirect(success_url)

class DeleteTop(LoginRequiredMixin, DeleteView):
    model = models.Top

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('indoor:top_list', kwargs = {'pk':self.object.training.pk})
        self.object.delete()
        return HttpResponseRedirect(success_url)
