from django.contrib import admin
from django.urls import path #Brings in the path function, which you use to map URL patterns to view functions.
from . import views

urlpatterns =[
   
    path('books/', views.list_books, name='list_books'),  # function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # class-based view

]