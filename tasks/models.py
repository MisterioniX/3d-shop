from django.db import models
from accounts.models import UserProfile
from django.urls import reverse_lazy
from datetime import datetime


class Task(models.Model):
    """Определение модели заказа."""

    # Поля модели в базе данных
    name = models.CharField(max_length=50, verbose_name='Заказ')
    description = models.TextField(editable=True, verbose_name='Описание заказа')
    date = models.DateField(auto_now=False, auto_now_add=True, verbose_name='Дата добавления')
    deadline = models.DateField(auto_now=False, editable=True, default=f"{datetime.today().date()}", verbose_name='Срок выполнения')
    author = models.ForeignKey(UserProfile, verbose_name='Автор', on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        """Meta definition for Task."""

        verbose_name = 'Заказ'  # Отображение названия модели на сайте
        verbose_name_plural = 'Заказы'  # Отображение названия модели на сайте во множественном числе  
        ordering = ['date'] # Порядок отображения моделей

    def __str__(self):  # В строковом отображении модель возвращает своё название 
        return self.name


    def get_absolute_url(self): # Абсолютный адрес модели
        """Return absolute url for Task."""
        return reverse_lazy('tasks:detail', kwargs={'pk':self.pk})

