
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = []  # no authentication
    permission_classes = [AllowAny]  #  allow anyone

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication] # Token auth for protected endpoints
    permission_classes = [IsAuthenticated] # Require authentication
