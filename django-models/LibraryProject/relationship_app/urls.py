from django.urls import path
from .views import SignUpView, list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    # function-based view
    path('books/', list_books, name='list_books'),

    # class-based view (use .as_view())
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

]     
