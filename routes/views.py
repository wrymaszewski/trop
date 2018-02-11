from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
# from accounts.models import User
from django.db.models import Avg
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

from .models import Place, Ascent, Route
from . import forms

# Create your views here.

User = get_user_model()

class PlaceList(ListView):
    model = Place
    template_name = 'routes/place_list.html'

    def get_queryset(self):
        self.place_dict = {}
        country_object_list = Place.objects.all()
        countries = set()
        for country in country_object_list:
            countries.add(country.country)

        for country in sorted(countries):
            city_object_list = Place.objects.all().filter(country=country)
            cities = set()
            for city in city_object_list:
                cities.add(city.city)
            self.place_dict[country] = {}

            for city in sorted(cities):
                    places = Place.objects.all().filter(city=city)
                    place_list = []
                    for place in places:
                        place_list.append(place)
                    self.place_dict[country][city] = place_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place_dict'] = self.place_dict
        return context


class RouteList(ListView):
    template_name = 'routes/route_list.html'
    model = Route

    def get_queryset(self):
        routes = Route.objects.select_related().filter(location = self.kwargs['pk'])
        self.route_list = []
        for route in routes:
            route.rating = Ascent.objects.filter(route = route.pk).filter(rating__range = range(1,3)).aggregate(Avg('rating'))['rating__avg']
            if route.location:
                route.lat = route.location.location.split(',')[0]
                route.lng = route.location.location.split(',')[1]
            self.route_list.append(route)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.route_list:
            context['route_list'] = self.route_list
            context['lat'] = self.route_list[0].lat
            context['lng'] = self.route_list[0].lng
        return context

class UserAscentList(ListView):
    model = Ascent
    template_name = 'routes/user_ascent_list.html'

    def get_queryset(self):
        return Ascent.objects.select_related().filter(user__username__iexact = self.kwargs.get('username'))

class RouteAscentList(ListView):
    model = Ascent
    template_name = 'routes/route_ascent_list.html'

    def get_queryset(self):
        return Ascent.objects.select_related().filter(route = self.kwargs['pk'])

# CRUD
class CreateRoute(LoginRequiredMixin, CreateView):
    model = Route
    fields = ['location', 'name', 'route_type', 'protection', 'scale', 'grade']
    success_url = reverse_lazy('routes:new_ascent')

    def get_initial(self):
        location = Place.objects.latest()
        return {'location': location}

class CreatePlace(LoginRequiredMixin, CreateView):
    model = Place
    fields = ('name', 'city', 'country', 'location')
    success_url = reverse_lazy('routes:new_route')


class CreateAscent(LoginRequiredMixin, CreateView):
    model = Ascent
    form_class = forms.AscentForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.success_url = reverse_lazy('routes:user_ascents', kwargs={'pk': self.object.user.pk})
        self.object.save()
        return super().form_valid(form)

    def get_initial(self):
        route = Route.objects.latest()
        return {'route': route}


class DeleteAscent(LoginRequiredMixin, DeleteView):
    model = Ascent
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('routes:user_ascents', kwargs = {'pk':self.object.user.pk})
        self.object.delete()
        return HttpResponseRedirect(success_url)


class UpdateAscent(LoginRequiredMixin, UpdateView):
    model = Ascent
    fields = ['route', 'date', 'ascent_style', 'rating', 'description']
    template_name = 'routes/ascent_update_form.html'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.success_url = reverse_lazy('routes:user_ascents', kwargs={'pk': self.object.user.pk})
        self.object.save()
        return super().form_valid(form)
