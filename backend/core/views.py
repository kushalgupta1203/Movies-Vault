from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
import os

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'message': 'Movies Vault API is running',
            'version': '1.0.0'
        })

class VersionView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'version': '1.0.0',
            'api_version': 'v1',
            'django_version': '4.2.7'
        })

class ConfigView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'tmdb_configured': bool(settings.TMDB_API_KEY),
            'debug': settings.DEBUG,
            'cors_origins': settings.CORS_ALLOWED_ORIGINS
        })

class TMDBConfigView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'base_url': settings.TMDB_BASE_URL,
            'image_base_url': 'https://image.tmdb.org/t/p/',
            'configured': bool(settings.TMDB_API_KEY)
        })
