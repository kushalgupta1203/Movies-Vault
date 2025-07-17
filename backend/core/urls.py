from django.urls import path
from . import views

urlpatterns = [
    # Health check and utilities
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
    path('version/', views.VersionView.as_view(), name='version'),
    
    # Configuration endpoints
    path('config/', views.ConfigView.as_view(), name='config'),
    path('tmdb-config/', views.TMDBConfigView.as_view(), name='tmdb_config'),
]

