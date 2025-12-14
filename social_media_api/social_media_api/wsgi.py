"""
WSGI config for social_media_api project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load environment variables BEFORE setting Django settings
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings.prod')

application = get_wsgi_application()