"""Root URL configuration for RentFlow."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('properties/', include('apps.properties.urls')),
    path('tenants/', include('apps.tenants.urls')),
    path('invoices/', include('apps.invoices.urls')),
    path('payments/', include('apps.payments.urls')),
    path('maintenance/', include('apps.maintenance.urls')),
    path('listings/', include('apps.public_listings.urls')),
    # API endpoints
    path('api/v1/', include('apps.accounts.api_urls')),
    path('api/v1/', include('apps.properties.api_urls')),
    path('api/v1/', include('apps.tenants.api_urls')),
    path('api/v1/', include('apps.invoices.api_urls')),
    path('api/v1/', include('apps.payments.api_urls')),
    path('api/v1/', include('apps.maintenance.api_urls')),
    path('api/v1/', include('apps.dashboard.api_urls')),
    path('api/v1/', include('apps.public_listings.api_urls')),
    # Root redirect
    path('', include('apps.public_listings.urls_root')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
