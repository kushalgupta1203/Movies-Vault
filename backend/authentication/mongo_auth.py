"""
Custom JWT Authentication Backend for MongoDB
=============================================

This custom authentication backend works with MongoEngine User models
instead of Django's built-in User model.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from authentication.mongo_models import User as MongoEngineUser


class MongoUserWrapper:
    """
    Wrapper class to make MongoEngine User compatible with Django's authentication system
    """
    def __init__(self, mongo_user):
        self.mongo_user = mongo_user
        self.id = str(mongo_user.id)
        self.username = mongo_user.username
        self.email = mongo_user.email
        self.is_active = mongo_user.is_active
        self.is_staff = mongo_user.is_staff
        self.is_superuser = mongo_user.is_superuser
        self.first_name = mongo_user.first_name
        self.last_name = mongo_user.last_name
    
    def __str__(self):
        return self.username
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False


class MongoJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that works with MongoDB users
    """
    
    def get_user(self, validated_token):
        """
        Get MongoDB user from JWT token
        """
        try:
            user_id = validated_token.get('user_id')
            if not user_id:
                return None
            
            # Get user from MongoDB
            mongo_user = MongoEngineUser.objects(id=user_id).first()
            if not mongo_user:
                return None
            
            # Return wrapped user
            return MongoUserWrapper(mongo_user)
            
        except Exception as e:
            print(f"DEBUG: JWT auth error: {e}")
            return None


class MongoAuthenticationMiddleware:
    """
    Custom middleware to handle MongoDB authentication
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip authentication for certain paths
        if self.should_skip_auth(request.path):
            request.user = AnonymousUser()
        
        response = self.get_response(request)
        return response
    
    def should_skip_auth(self, path):
        """
        Paths that don't require authentication
        """
        skip_paths = [
            '/api/auth/register/',
            '/api/auth/login/',
            '/api/auth/health/',
            '/api/movies/',  # Allow movie browsing without auth
            '/admin/',
            '/static/',
        ]
        
        for skip_path in skip_paths:
            if path.startswith(skip_path):
                return True
        
        return False
