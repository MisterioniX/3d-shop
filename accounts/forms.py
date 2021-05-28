from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from accounts.models import UserProfile

User = get_user_model()


class UserLoginForm(forms.Form):
    """Определение формы для авторизации пользователя."""

    # TODO: Define form fields here
    username = forms.CharField(label="username", max_length=50, widget=forms.TextInput({
        'class': 'form-control',
        'place_holder': 'Введите логин'
    }))
    password = forms.CharField(label="password", max_length=50, widget=forms.PasswordInput({
        'class': 'form-control',
        'place_holder': 'Введите пароль'
    }))
    
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise ValidationError('Такого пользователя нет')
            if not check_password(password, qs[0].password):
                raise ValidationError('Неправильный пароль')
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError('Данный пользователь неактивен')
        return super().clean(*args, **kwargs)
     
    
class UserRegistrationForm(forms.ModelForm):
    """Определение формы для авторизации пользователя."""

    # TODO: Define form fields here
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput({
        'class': 'form-control',
        'place_holder': 'Введите логин'
    }))
    password = forms.CharField(label="Пароль", max_length=50, widget=forms.PasswordInput({
        'class': 'form-control',
        'place_holder': 'Введите пароль'
    }))
    password_second = forms.CharField(label="Повторите пароль", max_length=50, widget=forms.PasswordInput({
        'class': 'form-control',
        'place_holder': 'Повторите пароль'
    }))
    email = forms.EmailField(label="email", max_length=254, widget=forms.EmailInput({
        'class': 'form-control',
        'place_holder': 'Введите почту'
    }))
    
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_second')
    
    
    def clean_password_second(self):
        data = self.cleaned_data
        if data['password'] != data['password_second']:
            raise ValidationError('Пароли не совпадают')
        return data['password_second']


class ProfileForm(forms.ModelForm):
    # avatar = forms.ImageField(label="avatar", allow_empty_file=True, widget=forms.FileInput({
    #     'class': 'form-control',
    #     'place_holder': 'Добавьте свой аватар'
    # }))
    
    class Meta:
        model = UserProfile
        fields = ['phonenumber']
        widgets = {
            'phonenumber': forms.TextInput({
            'class': 'form-control',
            'place_holder': 'Введите номер'
        }),
            'avatar': forms.FileInput({
            'class': 'form-control-file',
            'place_holder': 'Добавьте свой аватар'
        })
        }
        
        
    