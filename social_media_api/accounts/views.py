from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView , TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView  
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import CustomUserCreationForm
# Create your views here.
class RegisterView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = "You are registered successfully"

class SignInView(LoginView):
    
    template_name = 'login.html' 
    

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        token, created = Token.objects.get_or_create(user=user)
        self.request.session['auth_token'] = token.key  # optional
        messages.info(self.request, "An API token has been created for your account (stored in session).")
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user

        # Try to get the token (ensure it exists), show it on the profile page
        token, _ = Token.objects.get_or_create(user=user)
        context['user'] = user
        context['token'] = token.key

        return context