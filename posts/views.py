from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (TemplateView, ListView, DetailView,
                                CreateView, UpdateView, DeleteView)
from .models import Post, Comment
# from blog.forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from accounts.models import Group
from django.http import HttpResponseRedirect

# posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']

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
    field = ['title', 'text']

    def form_valid(self, form):
         self.object = form.save(commit=False)
         self.success_url = reverse_lazy('accounts:single_group',
                            kwargs = {'slug': self.kwargs.get('slug')})
         self.object.author = self.request.user
         self.object.group = Group.objects.get(slug=self.kwargs.get('slug'))
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
    fields = ['text']

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
    fields = ['text']

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
