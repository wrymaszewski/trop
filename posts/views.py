from django.views.generic import (ListView, DetailView,
                                CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from . import forms
from .models import Post, Comment
from accounts.models import Group

# posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = forms.PostForm

    def form_valid(self, form):
         self.object = form.save(commit=False)
         self.success_url = reverse_lazy('accounts:single_group',
                            kwargs = {'slug': self.kwargs.get('slug')})
         self.object.author = self.request.user
         self.object.group = Group.objects.get(slug=self.kwargs.get('slug'))
         self.object.save()
         return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = forms.PostForm

    def form_valid(self, form):
         self.object = form.save(commit=False)
         self.object.group = Group.objects.get(slug=self.object.group.slug)
         self.success_url = reverse_lazy('accounts:single_group',
                            kwargs = {'slug': self.object.group.slug})
         self.object.author = self.request.user
         self.object.save()
         return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('accounts:single_group', kwargs = {'slug':self.object.group.slug})
        self.object.delete()
        return HttpResponseRedirect(success_url)

#comments
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = forms.CommentForm

    def form_valid(self, form):
         self.object = form.save(commit=False)
         self.success_url = reverse_lazy('accounts:single_group',
                            kwargs = {'slug': self.kwargs.get('slug')})
         self.object.author = self.request.user
         self.object.post = Post.objects.get(pk = self.kwargs.get('pk'))
         self.object.save()
         return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = forms.CommentForm

    def form_valid(self, form):
         self.object = form.save(commit=False)
         self.success_url = reverse_lazy('accounts:single_group',
                            kwargs = {'slug': self.kwargs.get('slug')})
         self.object.author = self.request.user
         self.object.post = Post.objects.get(pk = self.kwargs.get('pk'))
         self.object.save()
         return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('accounts:single_group', kwargs = {'slug':self.object.group.slug})
        self.object.delete()
        return HttpResponseRedirect(success_url)
