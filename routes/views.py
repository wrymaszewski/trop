from django.shortcuts import render
from . import forms
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Place, Ascent, Route
from accounts.models import User
from django.db.models import Avg
from django.core.urlresolvers import reverse, reverse_lazy
# Create your views here.

from django.contrib.auth import get_user_model
User = get_user_model()

class PlaceList(ListView):
    model = Place
    template_name = 'routes/place_list.html'

    def get_queryset(self):
        self.place_dict = {}
        countries = Place.objects.values('country').distinct()
        for country in countries:
            country = country['country']
            cities = Place.objects.all().filter(country=country).values('city')
            self.place_dict[country] = []
            for city in cities:
                    city = city['city']
                    places = Place.objects.all().filter(city=city)
                    place_list = []
                    for place in places:
                        place_list.append(place)
                    self.place_dict[country].append({city:place_list})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place_dict'] = self.place_dict
        return context

class PlaceDetail(DetailView):
    model = Place


class RouteList(ListView):
    template_name = 'routes/route_list.html'
    model = Route

    def get_queryset(self):
        routes = Route.objects.select_related().filter(location = self.kwargs['pk'])
        self.route_list = []
        for route in routes:
            route.rating = Ascent.objects.filter(route = route.pk).aggregate(Avg('rating'))['rating__avg']
            route.lat = route.location.location.split(',')[0]
            route.lng = route.location.location.split(',')[1]
            self.route_list.append(route)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['route_list'] = self.route_list
        context['lat'] = self.route_list[0].lat
        context['lng'] = self.route_list[0].lng
        return context


class UserAscentList(ListView):
    model = Ascent
    template_name = 'routes/user_ascent_list.html'

    def get_queryset(self):
        return Ascent.objects.select_related().filter(user = self.kwargs['pk'])

class RouteAscentList(ListView):
    model = Ascent
    template_name = 'routes/route_ascent_list.html'

    def get_queryset(self):
        return Ascent.objects.select_related().filter(route = self.kwargs['pk'])


class CreateAscent(LoginRequiredMixin, CreateView):
    model = Ascent
    fields = ['route', 'date', 'ascent_style', 'rating', 'description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.success_url = reverse_lazy('routes:user_ascents', kwargs={'pk': self.object.user.pk})
        self.object.save()
        return super().form_valid(form)
