from django import forms
from django.forms import widgets

from mdls.models import Mdl, Tag


class MdlSearchForm(forms.Form):
    """Форма поиска 3D модели."""
    
    text = forms.CharField(label='Введите текст для поиска',    # Текст, который мы хотим найти в названии или описании
                           max_length=100, 
                           required=False, 
                           widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    
    tags = forms.ModelMultipleChoiceField(  # Категории, которые мы хотим видеть
        label='Выберите нужные категории', 
        queryset=Tag.objects.all(), 
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class':'form-control js-example-basic-multiple' # Помимо класса из Bootstrap добавляем класс из SELECT2, чтобы улучшить форму.
        }))
    
    order = forms.ChoiceField(label='Сортировать по:',  # Выбираем порядок сортировки моделей
                              choices=[('date', 'Дате'), 
                              ('name', 'Названию'),], 
                              required=False, 
                              widget=forms.Select(attrs={
            'class':'form-control'
        }))
    

    def clean_field(self):
        data = self.cleaned_data.get("name")
        
        return data
    
    class Meta:
        """Meta definition for MdlSearchForm."""

        model = Mdl
        fields = '__all__'
        


class MdlForm(forms.ModelForm): 
    """Форма для редактирования моделей."""
    # Атрибуты тэгов полей формы

    widgets_dct = {
            'name': forms.TextInput({
            'class': 'form-control',
            'place_holder': 'Введите название'
                }),
            'description': forms.Textarea({
            'class': 'form-control',
            'place_holder': 'Введите описание'
                }),
            'file': forms.FileInput({
                'class': 'form-control-file',
                'place_holder':'Добавьте модель'
                }),
            'tags': forms.SelectMultiple({
                'class': 'form-control js-example-basic-multiple' 
                }),
            'image': forms.FileInput({
                'class': 'form-control-file',
                'place_holder':'Добавьте фото модели'
                })
        }
    
    # Поля формы

    name = forms.CharField(max_length=50, label='Модель', widget=widgets_dct['name'])
    description = forms.CharField(label='Описание модели', widget=widgets_dct['description'])
    file = forms.FileField(label='Файл модели', widget=widgets_dct['file'])
    tags = forms.ModelMultipleChoiceField(Tag.objects.all(), label='Категории модели', widget=widgets_dct['tags'])
    image = forms.ImageField(label='Изображение модели', widget=widgets_dct['image'])
    
    
    class Meta:
        """Meta definition for Mdlform."""

        model = Mdl
        fields = ('name', 'description', 'file', 'tags', 'image')
    
        
