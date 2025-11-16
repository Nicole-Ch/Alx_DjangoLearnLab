# bookshelf/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.form_example, name='form_example'),
    path('books/<int:book_id>/edit/', views.form_example, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('search/', views.safe_search, name='safe_search'),
]