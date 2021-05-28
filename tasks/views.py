from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from tasks.forms import TaskForm, TaskSearchForm
from django.urls import reverse_lazy

from tasks.models import Task

 
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "Tasks/create.html"
    success_url = reverse_lazy('tasks:home')
    login_url = reverse_lazy('accounts:login')
    
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)
    
    

class TaskListView(ListView):
    model = Task
    template_name = "tasks/home.html"
    paginate_by = 10
    
    def get_queryset(self):
        text = self.request.GET.get('text', '')
        new_context = Task.objects.filter(Q(name__contains=text) | Q(description__contains=text))
        return new_context
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        form = TaskSearchForm(self.request.GET)
        context['form'] = form
        
        context['order'] = self.request.GET.get('order', 'date')
        
        return context    
    
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy('tasks:home')
    login_url = reverse_lazy('accounts:login')
    
    
    def get(self, request, *args, **kwargs):
        print(request.user, self.get_object().author)
        if request.user == self.get_object().author.user:
            return super().get(request, *args, **kwargs)
        return redirect('tasks:home')

    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().post(request, *args, **kwargs)
        return redirect('tasks:home')
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = ""
    success_url = reverse_lazy('tasks:home')
    login_url = reverse_lazy('accounts:login')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().author.user:
            return super().post(request, *args, **kwargs)
        return redirect('tasks:home')
    
    
