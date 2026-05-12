"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

# FIX: Point to production settings by default
# Railway's .env will override this, but this ensures local Docker works too
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()