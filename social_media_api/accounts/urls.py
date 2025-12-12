from django.urls import path
from .views import FollowUserAPIView, SignInView , RegisterView, ProfileAPIView, UnfollowUserAPIView


urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),


     path('follow/<int:user_id>/', FollowUserAPIView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserAPIView.as_view(), name='unfollow-user'),
    
]