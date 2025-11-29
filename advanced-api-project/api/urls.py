from django.urls import path,include

from .views import CreateView,DeleteView,DetailView,ListView,UpdateView



urlpatterns =[
    path('books/', ListView.as_view()),
    path('books/<int:pk>/', DetailView.as_view()),
    path('books/create/', CreateView.as_view()),
    path('books/<int:pk>/Update', UpdateView.as_view()),
    path('books/<int:pk>/Delete', DeleteView.as_view()),


]