from django.urls import path

from . import views

app_name = 'public_listings'

urlpatterns = [
    path('', views.PublicListingListView.as_view(), name='list'),
    path('<int:pk>/', views.PublicListingDetailView.as_view(), name='detail'),
]
