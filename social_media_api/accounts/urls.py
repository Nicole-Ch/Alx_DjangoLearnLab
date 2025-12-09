from django.urls import path
from .views import SignInView , RegisterView, ProfileAPIView


urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]