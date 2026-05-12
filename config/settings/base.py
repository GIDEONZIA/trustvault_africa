import os
import environ
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False),
    # Fix: Parse ALLOWED_HOSTS as string then split
    ALLOWED_HOSTS=(str, ''),
    DATABASE_URL=(str, ''),
)

# Read .env file (optional - won't crash if missing)
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Fix: Parse ALLOWED_HOSTS properly
ALLOWED_HOSTS = [host.strip() for host in env('ALLOWED_HOSTS').split(',') if host.strip()] or ['*']

# Application definition
DJANGO_APPS = [
    'jazzmin',
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
    'celery',
    'django_celery_beat',
]

LOCAL_APPS = [
    'apps.accounts',
    'apps.core',
    'apps.properties',
    'apps.tenants',
    'apps.payments',
    'apps.invoices',
    'apps.maintenance',
    'apps.dashboard',
    'apps.public_listings',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

JAZZMIN_SETTINGS = {
    "site_title": "TrustVault Africa",
    "site_header": "TrustVault Africa",
    "site_brand": "TrustVault™",
    "site_logo": "images/logo.svg",
    "site_logo_classes": "img-circle",
    "welcome_sign": "TrustVault Africa · Secure Property Payments",
    "copyright": "TrustVault Africa Ltd",
    "search_model": ["accounts.User", "properties.Property"],
    "user_avatar": None,
    "show_userthemes": False,
    "custom_css": "css/jazzmin-custom.css",
    
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"], "icon": "fas fa-th-large"},
        {"name": "Public Site", "url": "/", "new_window": True, "icon": "fas fa-external-link-alt"},
    ],
    
    "usermenu_links": [
        {"name": "Profile", "url": "accounts:profile_update", "icon": "fas fa-id-card"},
        {"model": "accounts.User"},
    ],
    
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    "order_with_respect_to": [
        "accounts",
        "auth",
        "properties",
        "financials",
        "maintenance",
    ],
    
    "icons": {
        "accounts.User": "fas fa-fingerprint",
        "accounts.LandlordProfile": "fas fa-crown",
        "accounts.TenantProfile": "fas fa-id-badge",
        "auth.Group": "fas fa-layer-group",
        "properties.Property": "fas fa-city",
        "properties.Unit": "fas fa-cube",
        "properties.Lease": "fas fa-file-contract",
        "financials.Invoice": "fas fa-file-invoice",
        "financials.Transaction": "fas fa-exchange-alt",
        "financials.Receipt": "fas fa-qrcode",
        "maintenance.MaintenanceRequest": "fas fa-robot",
        "maintenance.MaintenanceTask": "fas fa-microchip",
        "maintenance.Expense": "fas fa-chart-line",
        "listings.PublicListing": "fas fa-satellite-dish",
        "listings.Inquiry": "fas fa-comment-dots",
    },
    
    "default_icon_parents": "fas fa-folder-open",
    "default_icon_children": "fas fa-angle-right",
    
    "ui_tweaks": {
        "navbar_small_text": False,
        "footer_small_text": True,
        "body_small_text": False,
        "brand_small_text": False,
        "brand_colour": "navbar-dark",
        "accent": "accent-cyan",
        "navbar": "navbar-dark navbar-black",
        "no_navbar_border": True,
        "sidebar": "sidebar-dark-black",
        "sidebar_nav_small_text": False,
        "sidebar_disable_expand": False,
        "sidebar_nav_child_indent": True,
        "sidebar_nav_compact_style": True,
        "sidebar_nav_legacy_style": False,
        "sidebar_nav_flat_style": True,
    },
    
    "related_modal_active": False,
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "slate",
    "dark_mode_theme": "slate",
    "navbar": "navbar-dark navbar-black",
    "sidebar": "sidebar-dark-black",
    "brand_colour": "navbar-black",
    "accent": "accent-cyan",
    "button_classes": {
        "primary": "btn-primary btn-glow",
        "secondary": "btn-secondary",
        "info": "btn-info btn-glow",
        "warning": "btn-warning",
        "danger": "btn-danger btn-glow",
        "success": "btn-success btn-glow",
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
# Fix: Use env.db() safely with default empty string
DATABASE_URL = env('DATABASE_URL', default='')
if DATABASE_URL:
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
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

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
CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Security headers - REMOVED from base.py, moved to production.py only
# These were overriding production settings!
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_HSTS_SECONDS = 0
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_HSTS_PRELOAD = False

# Keep these non-HTTPS headers for local dev
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# M-Pesa Configuration
MPESA_CONFIG = {
    'CONSUMER_KEY': env('MPESA_CONSUMER_KEY', default=''),
    'CONSUMER_SECRET': env('MPESA_CONSUMER_SECRET', default=''),
    'PASSKEY': env('MPESA_PASSKEY', default=''),
    'SHORTCODE': env('MPESA_SHORTCODE', default=''),
    'ENVIRONMENT': env('MPESA_ENVIRONMENT', default='sandbox'),
}

# Africa's Talking (SMS)
AT_CONFIG = {
    'USERNAME': env('AT_USERNAME', default=''),
    'API_KEY': env('AT_API_KEY', default=''),
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='TrustVault Africa <noreply@trustvault.africa>')