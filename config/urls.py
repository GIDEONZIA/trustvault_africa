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

urlpatterns = [
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

# Support for Media (Photos/Uploads) and Static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
