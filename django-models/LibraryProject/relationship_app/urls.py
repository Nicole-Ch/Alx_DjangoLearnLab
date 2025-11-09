from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    # function-based view
    path('books/', list_books, name='list_books'),

    # class-based view (use .as_view())
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
