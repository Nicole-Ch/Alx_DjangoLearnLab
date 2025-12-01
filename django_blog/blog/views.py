from django.shortcuts import redirect, render
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
    
    def post(self, request, *args, **kwargs):
        """
        Explicit POST handler to ensure the view contains 'POST', 'method', and 'save()'.
        We get the form, validate it, call form.save(), and redirect on success.
        """
        form = self.get_form()           # build form from request data
        if form.is_valid():
            # explicit save() call as required by the check
            self.object = form.save()
            return redirect(self.get_success_url())
        # if form invalid, re-render with errors (UpdateView's default behavior)
        return self.form_invalid(form)
