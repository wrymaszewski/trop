from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import Sector, Ascent, Route
from . import forms
from .scales import convert_scale
from chartit import Chart, DataPool
from . import charts

# Create your views here.

User = get_user_model()

class SectorList(ListView):
    model = Sector
    template_name = 'routes/sector_list.html'

    def get_queryset(self):
        self.sector_dict = {}
        country_object_list = Sector.objects.all()
        countries = set()
        for country in country_object_list:
            countries.add(country.country)

        for country in sorted(countries):
            region_object_list = Sector.objects.all().filter(country=country)
            cities = set()
            for region in region_object_list:
                cities.add(region.region)
            self.sector_dict[country] = {}

            for region in sorted(cities):
                    sectors = Sector.objects.all().filter(region=region)
                    sector_list = []
                    for sector in sectors:
                        sector_list.append(sector)
                    self.sector_dict[country][region] = sector_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sector_dict'] = self.sector_dict
        return context

class RouteList(ListView):
    template_name = 'routes/route_list.html'
    model = Route

    def get_queryset(self):
        self.routes =  Route.objects.select_related().filter(sector__slug__iexact = self.kwargs.get('slug'))
        self.route_list = []
        for route in self.routes:
            route.rating = Ascent.objects.filter(route = route.pk).filter(rating__range = range(1,3)).aggregate(Avg('rating'))['rating__avg']
            self.route_list.append(route)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sector = Sector.objects.get(slug=self.kwargs.get('slug'))
        context['sector'] = self.sector
        context['lat'] = self.sector.location.split(',')[0]
        context['lng'] = self.sector.location.split(',')[1]
        if self.route_list:
            context['route_list'] = self.route_list
        context['chart'] = charts.route_pie_chart(self.kwargs.get('slug'))
        return context

class UserAscentList(ListView):
    model = Ascent
    template_name = 'routes/user_ascent_list.html'

    def get_queryset(self):
        return Ascent.objects.select_related().filter(user__username__iexact = self.kwargs.get('username'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user_prof'] = User.objects.get(username = self.kwargs.get('username'))
        context['chart_list'] = [
                                charts.user_ascent_chart(self.kwargs.get('username')),
                                charts.user_ascent_pie_chart(self.kwargs.get('username'))
                                ]
        return context

class RouteAscentList(ListView):
    model = Ascent
    template_name = 'routes/route_ascent_list.html'

    def get_queryset(self):
        self.route = Route.objects.get(slug = self.kwargs.get('route_slug'))
        self.route.rating = Ascent.objects.filter(route = self.route.pk).filter(rating__range = range(1,3)).aggregate(Avg('rating'))['rating__avg']
        return Ascent.objects.select_related().filter(route__slug__iexact = self.kwargs.get('route_slug'),
         route__sector__slug__iexact = self.kwargs.get('sector_slug'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object'] = self.route
        context['sector'] = Sector.objects.get(slug = self.kwargs.get('sector_slug'))
        context['chart_list'] = [
                                charts.route_ascent_chart(self.kwargs.get('route_slug')),
                                charts.ascent_pie_chart(self.kwargs.get('route_slug'))
                                ]
        return context


# CRUD
class CreateRoute(LoginRequiredMixin, CreateView):
    model = Route
    form_class = forms.RouteForm
    success_url = reverse_lazy('routes:new_ascent')

    def get_initial(self):
        if Sector.objects.all():
            sector = Sector.objects.latest()
            return {'sector': sector}

class CreateRouteFromSector(LoginRequiredMixin, CreateView):
    model = Route
    fields = ['sector', 'name', 'route_type', 'protection', 'scale', 'grade']

    def get_initial(self):
        sector = Sector.objects.get(slug = self.kwargs.get('slug'))
        self.success_url = reverse_lazy('routes:route_list',
        kwargs = {'slug': sector.slug})
        return {'sector': sector}

class CreateSector(LoginRequiredMixin, CreateView):
    model = Sector
    form_class = forms.SectorForm
    success_url = reverse_lazy('routes:new_route')


class CreateAscent(LoginRequiredMixin, CreateView):
    model = Ascent
    form_class = forms.AscentForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.success_url = reverse_lazy('routes:user_ascents', kwargs={'username': self.object.user.username})
        self.object.save()
        return super().form_valid(form)

    def get_initial(self):
        if Route.objects.all():
            route = Route.objects.latest()
            return {'route': route}

class CreateAscentFromRoute(LoginRequiredMixin, CreateView):
    model = Ascent
    form_class = forms.AscentForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.success_url = reverse_lazy('routes:user_ascents', kwargs={'username': self.object.user.username})
        self.object.save()
        return super().form_valid(form)

    def get_initial(self):
        route = Route.objects.get(slug = self.kwargs.get('route_slug'),
        sector__slug = self.kwargs.get('sector_slug'))
        return {'route': route}


class DeleteAscent(LoginRequiredMixin, DeleteView):
    model = Ascent
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('routes:user_ascents', kwargs = {'username':self.object.user.username})
        self.object.delete()
        return HttpResponseRedirect(success_url)


class UpdateAscent(LoginRequiredMixin, UpdateView):
    model = Ascent
    form_class = forms.AscentForm
    template_name = 'routes/ascent_update_form.html'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.success_url = reverse_lazy('routes:user_ascents', kwargs={'username': self.object.user.username})
        self.object.save()
        return super().form_valid(form)
