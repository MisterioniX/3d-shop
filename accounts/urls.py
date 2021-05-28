from django.urls import path
from accounts.views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'), 
    path('register/', registration_view, name='register'),
    path('detail/', ProfileDetailView.as_view(), name='detail'),
    path('update/', ProfileUpdateView.as_view(), name='update')
]