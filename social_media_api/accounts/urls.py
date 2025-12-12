from django.urls import path
from .views import FollowUserAPIView, SignInView , RegisterView, ProfileAPIView, UnfollowUserAPIView
from . import views


urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),


     path('follow/<int:user_id>/', views.FollowUserAPIView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserAPIView.as_view(), name='unfollow-user'),
    path('follow-status/<int:user_id>/', views.UserFollowStatusAPIView.as_view(), name='follow-status'),
    path('users/<int:user_id>/followers/', views.UserFollowersListAPIView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', views.UserFollowingListAPIView.as_view(), name='user-following'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    
]