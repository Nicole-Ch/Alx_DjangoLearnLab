from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSets, CommentViewSets

router = DefaultRouter()
router.register(r'Posts', PostViewSets)
router.register(r'comments', CommentViewSets)

urlpattterns = [
    path('', include(router.urls))
]