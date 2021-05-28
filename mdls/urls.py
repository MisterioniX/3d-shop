from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from mdls.views import *

urlpatterns = [
    path('<int:pk>', MdlDetailView.as_view(), name='detail'),
    path('create/', MdlCreateView.as_view(), name='create'),
    path('update/<int:pk>/', MdlUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', MdlDeleteView.as_view(), name='delete')
]