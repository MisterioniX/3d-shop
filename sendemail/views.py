from typing import Any

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from sendemail.apps import SendemailConfig
from kolyma_store.settings import *
from django.core.mail import send_mail, BadHeaderError

from sendemail.forms import EmailForm

# Create your views here.

class FeedbackView(LoginRequiredMixin, TemplateView):
    template_name = "sendemail/feedback.html"
    
    
    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.method == 'GET':
            form = EmailForm()
        elif request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                from_email = request.user.email
                message = form.cleaned_data['message']
                try:
                    send_mail(f'{subject} от {from_email}', message,
                            DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
                except BadHeaderError:
                    return HttpResponse('Ошибка в теме письма.')
                return redirect('sendemail:success')
        else:
            return HttpResponse('Неверный запрос.')
        
        return super().dispatch(request, *args, **kwargs)
        
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.method == 'GET':
            form = EmailForm()
            
        elif self.request.method == 'POST':
            form = EmailForm(self.request.POST)
            
        context['form'] = form
        
        return context   
    
    
class SuccessView(TemplateView):
    template_name = "sendemail/success.html"


