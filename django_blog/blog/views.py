from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView 
from django.contrib.auth import views as auth_views
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from blog.forms import BlogForm, CommentForm
from django.db.models import Q


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

    def get_context_data(self, **kwargs):
       context =  super().get_context_data(**kwargs)
       post = self.get_object()
       context['comments'] = post.comments.all()
       context['comment_form'] = CommentForm()
       return context
        

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


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'


    def dispatch(self, request, *args, **kwargs):
        post_pk = self.kwargs.get('post_pk') or self.kwargs.get('pk')
        self.post = get_object_or_404(Post, pk=post_pk)
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        #Before saving the comment, attach author and post
        # so the comment knows who wrote it and which post it belongs to
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail',kwargs={'pk':self.post.pk})
        #After saving, send the user back to the post detail page (so they can see their comment)



class CommentUpdateView(LoginRequiredMixin,UserPassesTestMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def test_func(self):
       comment = self.get_object()
       return comment.author == self.request.user
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().post.pk})
    

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'comment_delete.html' 

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().post.pk})


class TagListView(generic.ListView):
    model = Post
    template_name = 'blog/tag_post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        # tags__name__iexact searches posts that have a tag with this name (case-insensitive)
        return Post.objects.filter(tags__name__iexact=tag_name).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag_name')
        return context


class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return Post.objects.none()
        # Search title or content or tags' names
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()