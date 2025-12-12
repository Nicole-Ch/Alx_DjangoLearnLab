from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSets, CommentViewSets
from . import views

router = DefaultRouter()
router.register(r'Posts', PostViewSets)
router.register(r'comments', CommentViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.UserFeedView.as_view(), name='user-feed'),
]