from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView , TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import CustomUserCreationForm
from accounts.serializers import LoginSerializer, UserSerializer
# Create your views here.
class RegisterView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = "You are registered successfully"

class SignInView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = serializer.validated_data['token']  # LoginSerializer put token there
        return Response({'token': token, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user

        # Try to get the token (ensure it exists), show it on the profile page
        token, _ = Token.objects.get_or_create(user=user)
        context['user'] = user
        context['token'] = token.key

        return context