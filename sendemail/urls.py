from django.contrib import admin
from django.urls import path

from .views import FeedbackView, SuccessView

urlpatterns = [
    path('', FeedbackView.as_view(), name='feedback'),
    path('success/', SuccessView.as_view(), name='success'),
]