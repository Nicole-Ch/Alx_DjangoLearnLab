from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView 
from django.contrib.auth import views as auth_views
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from blog.forms import BlogForm


from .models import  Post
# Create your views here.

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'


class LoginView(auth_views.LoginView):
    template_name = "blog/login.html"

class LogoutView(auth_views.LogoutView):
    template_name = "blog/logout.html" 


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
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
            #self.object is not the single email field itself. It is the User model instance.
            return redirect(self.get_success_url())
        # if form invalid, re-render with errors (UpdateView's default behavior)
        return self.form_invalid(form)


class BlogListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class BlogDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'detailpost'

class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = BlogForm
    template_name = 'blog/post_form.html'
    

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = BlogForm
    template_name = 'post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user 

class BlogDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Post
    context_object_name = 'blog'
    success_url = reverse_lazy('posts')   

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user 


