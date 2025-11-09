from django.urls import path
from .views import SignUpView, list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    # function-based view
    path('books/', list_books, name='list_books'),

    # class-based view (use .as_view())
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    # Registration
    path('signup/', SignUpView.as_view(), name='register'),

    # Login (built-in view)
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout (built-in view, with template)
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    

]     
