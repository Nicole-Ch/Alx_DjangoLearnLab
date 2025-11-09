from django.urls import path

from LibraryProject.bookshelf import views
from .views import SignUpView, list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    # function-based view
    path('books/', list_books, name='list_books'),

    # class-based view (use .as_view())
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),


    # Registration
    path('signup/', views.register, name='register'),

    # Login
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Profile page
    path('accounts/profile/', 
         LoginView.as_view(template_name='relationship_app/profile.html'), 
         name='profile'),


     path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),     

    

]     
