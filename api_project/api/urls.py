from django.urls import include, path
from .views import BookList , BookViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token 


from api import views

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),

    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),  # This includes all routes registered with the router
    
    # Authentication endpoint
     path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]