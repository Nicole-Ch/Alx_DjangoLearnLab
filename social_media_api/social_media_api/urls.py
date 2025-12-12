    # social_media_api/urls.py
from django.contrib import admin
from django.urls import path, include

from accounts.views import FeedAPIView

urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/accounts/', include('accounts.urls')),
          path('feed/', FeedAPIView.as_view(), name='feed'),
        path('accounts/', include('accounts.urls')),
        path('api/', include('posts.urls')),
    ]