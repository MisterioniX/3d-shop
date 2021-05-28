from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from tasks.views import *

urlpatterns = [
    # path('<int:pk>', TaskDetailView.as_view(), name='detail'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete'),
    path('', TaskListView.as_view(), name='home')
]