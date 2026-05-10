"""Development settings"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Override database for development (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
