"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.utils import timezone
from django.db import connection, OperationalError


# Health check endpoint for Railway
def health_check(request):
    health_status = {
        "status": "healthy",
        "service": "trustvault-api",
        "timestamp": timezone.now().isoformat(),
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status["database"] = "connected"
    except OperationalError:
        health_status["database"] = "disconnected"
        health_status["status"] = "degraded"
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return JsonResponse(health_status, status=status_code)


urlpatterns = [
    # Health check (must be FIRST - Railway checks this immediately)
    path('health/', health_check, name='health_check'),

    # Core Admin
    path('admin/', admin.site.urls),

    # Authentication & User Management
    path('accounts/', include('allauth.urls')),
    path('user-profiles/', include('apps.accounts.urls')),

    # Business Logic Apps
    path('dashboard/', include('apps.dashboard.urls')),
    path('properties/', include('apps.properties.urls')),
    path('tenants/', include('apps.tenants.urls')),
    path('payments/', include('apps.payments.urls')),
    path('invoices/', include('apps.invoices.urls')),
    path('maintenance/', include('apps.maintenance.urls')),

    # Public Facing App (Landing Page)
    path('', include('apps.public_listings.urls')),
]

# Static/Media: Only add Django's dev server in DEBUG
# Whitenoise handles static in production via middleware
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Note: static() for STATIC_URL not needed - Whitenoise handles it