from typing import Any, Dict
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, UpdateView
from mdls.forms import MdlForm

from mdls.models import Mdl


class MdlDetailView(LoginRequiredMixin, DetailView):    # Страница модели
    login_url = reverse_lazy('accounts:login')
    model = Mdl
    template_name = "mdls/detail.html"


class MdlCreateView(LoginRequiredMixin, CreateView):    # Страница создания модели
    model = Mdl
    form_class = MdlForm
    template_name = "mdls/create.html"
    success_url = reverse_lazy('home')  # Редирект в случае успеха
    # Редирект для неавторизованных пользователей
    login_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile    # Получаем автора
        form.instance.extension = form.instance.file.path.split(
            '.')[-1].lower()    # Получаем расширение модели
        return super().form_valid(form)  # вызываем функцию из родительского класса


class MdlUpdateView(LoginRequiredMixin, UpdateView):    # Страница редактирования модели
    model = Mdl
    form_class = MdlForm
    template_name = "mdls/update.html"
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author.user:   # Если запрос отправлен автором 3D модели
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')

    def form_valid(self, form):
        form.instance.extension = form.instance.file.path.split(
            '.')[-1].lower()    # Получаем расширение модели
        return super().form_valid(form)  # вызываем функцию из родительского класса


class MdlDeleteView(LoginRequiredMixin, DeleteView):    # Удаление модели
    model = Mdl
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):    # GET запрос вызывает POST запрос
        return self.post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author.user:   # Если запрос отправлен автором 3D модели
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')
