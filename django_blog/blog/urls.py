# blog/urls.py
from django.urls import path
from .views import CommentCreateView, CommentDeleteView, CommentUpdateView, RegisterView, LoginView, LogoutView, ProfileUpdateView , BlogCreateView,BlogDeleteView,BlogDetailView,BlogListView,BlogUpdateView, SearchResultsView, TagListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('post/', BlogListView.as_view(), name="posts"),
    path('post/new/', BlogCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/', BlogDetailView.as_view(), name="post-detail"),
    path('post/<int:pk>/update/',BlogUpdateView.as_view(), name="post-edit"),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name="post-delete"),


    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),


    path('tags/<str:tag_name>/', TagListView.as_view(), name='posts-by-tag'),
    path('search/', SearchResultsView.as_view(), name='post-search'),

]
