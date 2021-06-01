from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from accounts.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin


from accounts.forms import UserLoginForm, UserRegistrationForm, ProfileForm


class ProfileDetailView(TemplateView):
    model = UserProfile
    template_name = "accounts/profile.html"


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    model = UserProfile
    template_name = "accounts/update.html"
    success_url = reverse_lazy('accounts:detail')
    
    def dispatch(self, request, *args, **kwargs):
        p_form = ProfileForm(data=self.request.POST, instance=self.request.user.profile)
        
        if self.request.method=='POST' and p_form.is_valid():
            p_form.save()
            return redirect('accounts:detail')
        return super().dispatch(request, *args, **kwargs)
    
    
    def form_valid(self, form):
        p_form = ProfileForm(data=self.request.POST, instance=self.request.user.profile)
        p_form.save()
        return redirect('accounts:detail')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        form = ProfileForm(data=self.request.POST, instance=self.request.user.profile)
        context['form'] = form
        
        return context    


def login_view(request):    # Вход 
    form = UserLoginForm(request.POST or None) # Форма входа
    _next = request.GET.get('next') # Страница, на которую мы перейдём после входа
    if form.is_valid():
        username = form.cleaned_data.get('username')    # Получаем username из формы
        password = form.cleaned_data.get('password')    # Получаем пароль из формы
        user = authenticate(username=username, password=password)   # Выполняем вход
        login(request, user)    
        _next = _next or '/'    # Редирект на следующую _next или на домашнюю
        return redirect(_next)  
    return render(request, 'accounts/login.html', {'form': form})   # Если форма недействительна, то рендерим страницу входа из шаблона


def logout_view(request):   # Выход 
    logout(request)
    return redirect('/')


def registration_view(request): # Регистрация
    if request.method == "POST":    # Если метод запроса POST
        u_form = UserRegistrationForm(request.POST) # Форма регистрации пользователя 
        p_form = ProfileForm(request.POST)  #   Форма регистрации профиля (профиль связывается с пользователем и содержит поле с мобильным телефоном)
        if u_form.is_valid() and p_form.is_valid(): 
            user = u_form.save(commit=False)    # Получаем объект пользователя из формы
            user.set_password(u_form.cleaned_data['password'])  # Устанавливаем пользователю пароль
            user.save() # Сохраняем пользователя
            p_form = p_form.save(commit=False)  # Получаем профиль из формы
            p_form.user = user  # Привязываем профиль к пользователю
            p_form.save()   # Сохраняем профиль
            return redirect('accounts:login')   # Редирект на страницу входа
    else:
        u_form = UserRegistrationForm() # Форма регистрации пользователя 
        p_form = ProfileForm()  # Форма регистрации профиля
    return render(request, 'accounts/register.html', {'u_form': u_form, 'p_form': p_form})  # Рендерим страницу регистрации из шаблона

