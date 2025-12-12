
from django.http import HttpResponse
from django.views.generic import CreateView 

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from accounts.forms import CustomUserCreationForm

from accounts.serializers import LoginSerializer, UserSerializer


# Create your views here.
class RegisterView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = "You are registered successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create a token for the new user
        user = form.save()  # make sure form.save() returns the user
        token, created = Token.objects.get_or_create(user=user)
        print(f"Token for {user.username}: {token.key}")  # optional, for debugging
        return response

class SignInView(APIView):
    permission_classes = [permissions.AllowAny]   #permissions.AllowAny means anyone (even unauthenticated users) can call this endpoint.

    def post(self, request):
        serializer = LoginSerializer(data=request.data)  #Creates an instance of your LoginSerializer. -(data=request.data)passes the incoming POST data (JSON with username/password) into the serializer.
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = serializer.validated_data['token']  # LoginSerializer put token there
        return Response({'token': token, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        token, _ = Token.objects.get_or_create(user=user)
        from accounts.serializers import UserSerializer
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    



