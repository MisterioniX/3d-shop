from django.db.models import QuerySet
from mdls.models import Mdl

from functools import reduce


def filter_by_tags(tags) -> QuerySet:
    return reduce(lambda x, y: x | y, [tag.model_tags.all() for tag in tags]).distinct()    
         

