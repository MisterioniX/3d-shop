from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from mdls.forms import MdlSearchForm
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required


from mdls.models import Mdl, Tag
from shop.utils import filter_by_tags


class MdlListView(ListView):
    model = Mdl # Модель 3D модели
    paginate_by = 20    # Количество 3D моделей на одной странице
    template_name = 'shop/home.html'    # Шаблон
    form_class = MdlSearchForm  # Форма поиска
    
    def get_queryset(self): # Формирование набора моделей, который мы отобразим
        tags_ids = self.request.GET.getlist('tags', # Получаем id категорий, которые хочет видеть пользователь
        Tag.objects.all().values_list('id', flat=True)) # Список названий категорий, которые выбрал пользователь
        order = self.request.GET.get('order', 'date')   # Получаем порядок, в котором надо отсортировать модели
        text = self.request.GET.get('text', '') # Получаем подстроку, которая должна присутствовать в названии или описании модели
        qs = filter_by_tags(Tag.objects.filter(    # Получаем набор моделей из функции filter_by_tags
            id__in=tags_ids,    #  Выбираем тэги, id которых содержится в tags_ids
        )).filter(Q(name__icontains=text) |  # Филитруем по наличию text в названии или описании
        Q(description__icontains=text)).order_by(order)  # Сортируем в заданном порядке
        return qs  # Возвращаем полученный набор моделей
        
        
    def get_context_data(self, **kwargs):   # Данные, которые будет испоьзовать view для формирования страницы
        context = super().get_context_data(**kwargs)    # Получаем данные из материнского метода
        
        form = MdlSearchForm(self.request.GET)  # Добавляем форму поиска
        context['form'] = form  
        
        context['tags'] = self.request.GET.get('tags', Tag.objects.all().values_list('id', flat=True))  # Категории моделей
        context['order'] = self.request.GET.get('order', 'date')    # Порядок сортировки
        
        return context    # Возвращаем контекст с новыми данными
    
