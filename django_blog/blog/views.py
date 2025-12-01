from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView , UpdateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# Create your views here.

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'


class LoginView(auth_views.LoginView):
    template_name = "blog/login.html"

class LogoutView(auth_views.LogoutView):
    template_name = "blog/logout.html" 


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["email"]
    template_name = "blog/profile.html"
    success_url = reverse_lazy('profile')


    def get_object(self, queryset=None):
        # edit the current logged-in user
        return self.request.user
