from django.db.models import QuerySet
from mdls.models import Mdl

from functools import reduce


def filter_by_tags(tags) -> QuerySet:   
    if tags:    # Если пользователь выбрал категории
        return reduce(lambda x, y: x | y, [tag.model_tags.all() for tag in tags]).distinct() # Возвращаем объединённые наборы данных, состоящие из моделей, принадлежащих каждой из категорий, исключив дублирующиеся модели
    return Mdl.objects.all() # Если категоии не были выбраны, возвращаем все модели из базы

