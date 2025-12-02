# blog/urls.py
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileUpdateView , BlogCreateView,BlogDeleteView,BlogDetailView,BlogListView,BlogUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('posts/', BlogListView.as_view(), name="posts"),
    path('posts/create/', BlogCreateView.as_view(), name="post-create"),
    path('posts/<int:pk>/', BlogDetailView.as_view(), name="post-detail"),
    path('posts/<int:pk>/edit/',BlogUpdateView.as_view(), name="post-edit"),
    path('posts/<int:pk>/delete/', BlogDeleteView.as_view(), name="post-delete")

]
