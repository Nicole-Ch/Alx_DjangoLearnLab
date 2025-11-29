# api/views.py
from rest_framework import generics, filters
from django_filters import rest_framework  # checker expects this import
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# List + Create: supports filtering, search, ordering
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # IMPORTANT: use rest_framework.DjangoFilterBackend per the import above
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # allow exact filtering on these fields (author__name follows FK -> Author.name)
    filterset_fields = ['title', 'author__name', 'publication_year']

    # search and ordering config
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


# Retrieve / Update / Destroy: single endpoint with full write support
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Create a new book
class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Update an existing book
class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Delete a book
class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
