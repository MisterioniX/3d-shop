from datetime import datetime
from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    """Form definition for Task."""
    
    name = forms.CharField(max_length=50, label='Название заказа', widget=forms.TextInput({
        'class': 'form-control',
        'place_holder': 'Введите название'
        }))
    description = forms.CharField(label='Описание заказа', widget=forms.Textarea({
        'class': 'form-control',
        'place_holder': 'Введите описание'
        }))
    deadline = forms.DateField(label='Срок выполнения заказа', required=False,
                               initial=f"{datetime.today().date()}",
                               widget=forms.SelectDateWidget(attrs={
        'class': 'd-inline-flex form-control col-xl-2 col-md-2 col-sm-3 m-1',
        'place_holder': 'Введите срок выполнения заказа'
        }, 
        empty_label=("Выберите год", "Выберите месяц", "Выберите день"),
        
        ))

    class Meta:
        """Meta definition for Taskform."""

        model = Task
        fields = ['name', 'description', 'deadline']
        
        
class TaskSearchForm(forms.Form):
    """Form definition for Task."""
    
    text = forms.CharField(label='Введите текст для поиска', 
                           max_length=100, 
                           required=False, 
                           widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    
    class Meta:
        """Meta definition for Taskform."""

        model = Task
        fields = ['name', 'description']
