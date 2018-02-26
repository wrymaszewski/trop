from django.views.generic import (ListView, DetailView,
                                CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Sector, Ascent, Route
from . import forms, charts

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class SectorList(ListView):
    # Code needs to be optimized!
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
        self.sector = Sector.objects.select_related().get(slug = self.kwargs.get('slug'))
        routes =  self.sector.routes.all()
        self.route_list = []
        for route in routes:
            route.rating = (route.ascents
                                .filter(rating__range = range(1,3))
                                .aggregate(Avg('rating'))['rating__avg'])
            self.route_list.append(route)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        self.user = User.objects.select_related().get(username = self.kwargs.get('username'))
        return self.user.ascents.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user_prof'] = self.user
        context['chart_list'] = [
                                charts.user_ascent_chart(self.user.username),
                                charts.user_ascent_pie_chart(self.user.username)
                                ]
        return context

class RouteAscentList(ListView):
    model = Ascent
    template_name = 'routes/route_ascent_list.html'

    def get_queryset(self):
        self.route = (Route.objects.select_related()
                                    .get(slug = self.kwargs.get('route_slug'),
                                     sector__slug = self.kwargs.get('sector_slug')))
        self.route.rating = (self.route.ascents
                                        .filter(rating__range = range(1,3))
                                        .aggregate(Avg('rating'))['rating__avg'])
        return self.route.ascents.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object'] = self.route
        context['chart_list'] = [
                                charts.route_ascent_chart(self.kwargs.get('route_slug')),
                                charts.ascent_pie_chart(self.kwargs.get('route_slug'))
                                ]
        context['lat'] = self.route.sector.location.split(',')[0]
        context['lng'] = self.route.sector.location.split(',')[1]
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

class CreateRouteRedirect(LoginRequiredMixin, CreateView):
    model = Route
    form_class = forms.RouteForm

    def get_initial(self):
        if Sector.objects.all():
            sector = Sector.objects.latest()
            return {'sector': sector}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.success_url = reverse_lazy('routes:route_list',
                             kwargs={'slug': self.object.sector.slug})
        self.object.save()
        return super().form_valid(form)


class CreateRouteFromSector(LoginRequiredMixin, CreateView):
    model = Route
    fields = ['sector', 'name', 'route_type', 'protection', 'scale', 'grade']

    def get_initial(self):
        sector = Sector.objects.get(slug =self.kwargs.get('slug'))
        self.success_url = reverse_lazy('routes:route_list',
                                     kwargs = {'slug': sector.slug})
        return {'sector': sector}

class CreateSector(LoginRequiredMixin, CreateView):
    model = Sector
    form_class = forms.SectorForm
    success_url = reverse_lazy('routes:new_route')

class CreateSectorRedirect(LoginRequiredMixin, CreateView):
    model = Sector
    form_class = forms.SectorForm
    success_url = reverse_lazy('routes:sectors')

class CreateAscent(LoginRequiredMixin, CreateView):
    model = Ascent
    form_class = forms.AscentForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.success_url = reverse_lazy('routes:user_ascents',
                                 kwargs={'username': self.object.user.username})
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
        self.success_url = reverse_lazy('routes:user_ascents',
                                 kwargs={'username': self.object.user.username})
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
        success_url = reverse_lazy('routes:user_ascents',
                                 kwargs = {'username':self.object.user.username})
        self.object.delete()
        return HttpResponseRedirect(success_url)


class UpdateAscent(LoginRequiredMixin, UpdateView):
    model = Ascent
    form_class = forms.AscentForm
    template_name = 'routes/ascent_update_form.html'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.success_url = reverse_lazy('routes:user_ascents',
                                     kwargs={'username': self.object.user.username})
        self.object.save()
        return super().form_valid(form)
