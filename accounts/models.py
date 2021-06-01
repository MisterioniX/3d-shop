from django.contrib.auth import get_user_model
from django.db import models
from django.urls.base import reverse_lazy

User = get_user_model()

class UserProfile(models.Model):

    # Поля модели в базе данных
    user = models.OneToOneField(User, verbose_name="Аккаунт", on_delete=models.CASCADE, related_name='profile')
    phonenumber = models.CharField(verbose_name="Номер телефона", max_length=12, default=None)
    
    
    def __str__(self): # В строковом отображении модель возвращает своё название 
        return self.user.username
    
    
    def get_absolute_url(self):  # Абсолютный адрес модели
        return reverse_lazy('accounts:detail')
    
    