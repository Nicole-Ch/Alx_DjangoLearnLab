from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LikePostAPIView, PostViewSets, CommentViewSets, UnlikePostAPIView
from . import views

router = DefaultRouter()
router.register(r'Posts', PostViewSets)
router.register(r'comments', CommentViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.UserFeedView.as_view(), name='user-feed'),

    path('posts/<int:pk>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostAPIView.as_view(), name='unlike-post'),
]