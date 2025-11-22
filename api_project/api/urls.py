from django.urls import include, path
from .views import BookList , BookViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views


from api import views

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),

    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),  # This includes all routes registered with the router

     path('api-token-auth/', views.obtain_auth_token, ame='api_token_auth')
]