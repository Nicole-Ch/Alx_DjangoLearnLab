from django.urls import path
from .views import SignInView , RegisterView, ProfileView


urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]