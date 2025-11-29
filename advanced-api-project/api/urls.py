from django.urls import path,include

from .views import BookListView, BookCreateView , BookRetrieveView, BookUpdateView, BookDestroyView



urlpatterns =[
    path('books/', BookListView.as_view()),
    path('books/<int:pk>/', BookRetrieveView.as_view()),
    path('books/create/', BookCreateView.as_view()),
    path('books/<int:pk>/Update', BookUpdateView.as_view()),
    path('books/<int:pk>/Update', BookDestroyView.as_view()),


]