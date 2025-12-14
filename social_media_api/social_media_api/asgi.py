"""
ASGI config for social_media_api project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from dotenv import load_dotenv  # Add this
from django.core.asgi import get_asgi_application

# Load environment variables
load_dotenv()

# Default to production settings for ASGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings.prod')

application = get_asgi_application()