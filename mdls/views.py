from typing import Any, Dict
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, UpdateView
from mdls.forms import MdlForm

from mdls.models import Mdl



class MdlDetailView(LoginRequiredMixin, DetailView):
    # login_url = reverse_lazy('accounts:login')
    model = Mdl
    template_name = "mdls/detail.html"
    
    
class MdlCreateView(LoginRequiredMixin, CreateView):
    model = Mdl
    form_class = MdlForm
    template_name = "mdls/create.html"
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.extension = form.instance.file.path.split('.')[-1].lower()
        return super().form_valid(form)
    
    
class MdlUpdateView(LoginRequiredMixin, UpdateView):
    model = Mdl
    form_class = MdlForm
    template_name = "mdls/update.html"
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
        print(request.user, self.get_object().author)
        if request.user == self.get_object().author.user:
            return super().get(request, *args, **kwargs)
        return redirect('home')

    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().post(request, *args, **kwargs)
        return redirect('home')
    
    def form_valid(self, form):
        form.instance.extension = form.instance.file.path.split('.')[-1].lower()
        return super().form_valid(form)
    
    
class MdlDeleteView(LoginRequiredMixin, DeleteView):
    model = Mdl
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('accounts:login')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().author.user:
            return super().post(request, *args, **kwargs)
        return redirect('home')


    

    