"""
RentFlow - Property Management SaaS
Base settings shared across all environments
"""

import os
import environ
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# Read .env file (optional - won't crash if missing)
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Application definition
DJANGO_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_htmx',
]

LOCAL_APPS = [
    'apps.core',
    'apps.accounts',
    'apps.properties',
    'apps.tenants',
    'apps.payments',
    'apps.invoices',
    'apps.maintenance',
    'apps.dashboard',
    'apps.public_listings',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

UNFOLD = {
    "SITE_TITLE": "Zia Property Ltd",
    "SITE_HEADER": "Zia Property Administration",
    "SITE_SYMBOL": "apartment",
    "SHOW_HISTORY": True,
    "TABS": [
            {
                "models": [
                    "properties.property",
                    "properties.unit",
                    "properties.propertyimage",
                    "properties.amenity",
                ],
                "items": [
                    {
                        "title": "Real Estate Overview",
                        "link": "/admin/properties/property_changelist",
                    },
                    {
                        "title": "Unit Inventory",
                        "link": "/admin/properties/unit_changelist",
                    },
                ],
            },
            {
                "models": [
                    "payments.transaction",
                    "payments.mpesapayment",
                    "invoices.invoice",
                ],
                "items": [
                    {
                        "title": "Cash Flow",
                        "link": "/admin/payments/transaction_changelist",
                    },
                    {
                        "title": "Billing",
                        "link": "/admin/invoices/invoice_changelist",
                    },
                ],
            },
        ],    "EXTENSIONS": {
        "modeltranslation": False,
    },
    "COLORS": {
        "primary": {
            "50": "250 252 255",
            "100": "240 249 255",
            "200": "186 230 253",
            "300": "125 211 252",
            "400": "56 189 248",
            "500": "14 165 233",  # Zia Blue
            "600": "2 132 199",
            "700": "3 105 161",
            "800": "7 89 131",
            "900": "12 74 110",
            "950": "8 51 68",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,  # Keeps it clean
        "navigation": [
            {
                "title": "Property Management",
                "collapsible": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": "/admin/",
                    },
                    {
                        "title": "Properties",
                        "icon": "home_work",
                        "link": "/admin/properties/property/",
                    },
                    {
                        "title": "Tenants",
                        "icon": "group",
                        "link": "/admin/tenants/lease/",
                    },
                ],
            },
            {
                "title": "Financials",
                "collapsible": True,
                "items": [
                    {
                        "title": "Invoices",
                        "icon": "description",
                        "link": "/admin/invoices/invoice/",
                    },
                    {
                        "title": "Payments",
                        "icon": "payments",
                        "link": "/admin/payments/transaction/",
                    },
                ],
            },
        ],
    },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database - with proper fallback
if env('DATABASE_URL'):
    DATABASES = {
        'default': env.db()
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Django AllAuth - Updated for latest version
SITE_ID = 1

# Use new-style allauth settings (v0.60+)
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Celery
CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Security headers (production)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# M-Pesa Configuration
MPESA_CONFIG = {
    'CONSUMER_KEY': env('MPESA_CONSUMER_KEY'),
    'CONSUMER_SECRET': env('MPESA_CONSUMER_SECRET'),
    'PASSKEY': env('MPESA_PASSKEY'),
    'SHORTCODE': env('MPESA_SHORTCODE'),
    'ENVIRONMENT': env('MPESA_ENVIRONMENT'),
}

# Africa's Talking (SMS)
AT_CONFIG = {
    'USERNAME': env('AT_USERNAME'),
    'API_KEY': env('AT_API_KEY'),
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
