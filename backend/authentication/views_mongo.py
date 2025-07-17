from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from .mongo_models import User, UserPreferences, BlacklistedToken
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer,
)
import json
from datetime import datetime


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Check if username already exists
        username = request.data.get('username')
        if not username:
            return Response({
                'error': 'Username is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects(username=username).first():
            print(f"DEBUG: Username '{username}' already exists")  # Debug log
            return Response({
                'error': 'Username already exists. Please choose a different username.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check email (optional)
        email = request.data.get('email', '')
        
        # Check password length
        password = request.data.get('password', '')
        if not password:
            return Response({
                'error': 'Password is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if len(password) < 8:
            return Response({
                'error': 'Password must be at least 8 characters long.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check username length
        if len(username) < 3:
            return Response({
                'error': 'Username must be at least 3 characters long.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create user with MongoEngine
            user = User(
                username=username,
                email=email if email else f"{username}@moviesvault.local",  # Generate email if not provided
                first_name=request.data.get('first_name', ''),
                last_name=request.data.get('last_name', ''),
            )
            user.set_password(password)
            user.save()
            
            # Create user preferences
            preferences = UserPreferences(user_id=str(user.id))
            preferences.save()
            
            # Generate JWT tokens
            # Create a temporary Django user object for JWT token generation
            django_user_data = {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
            
            # Create custom token payload
            refresh = RefreshToken()
            refresh['user_id'] = str(user.id)
            refresh['username'] = user.username
            
            return Response({
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_active': user.is_active,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"DEBUG: Registration error: {e}")
            return Response({
                'error': f'Registration failed: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Check if fields are provided
        if not username:
            return Response({
                'error': 'Username is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if not password:
            return Response({
                'error': 'Password is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists
        user = User.objects(username=username).first()
        if not user:
            print(f"DEBUG: User '{username}' does not exist")  # Debug log
            return Response({
                'error': 'Username does not exist. Please check your username or sign up.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if account is active
        if not user.is_active:
            print(f"DEBUG: User '{username}' account is disabled")  # Debug log
            return Response({
                'error': 'Your account has been disabled. Please contact support.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check password
        if user.check_password(password):
            print(f"DEBUG: User '{username}' authenticated successfully")  # Debug log
            
            # Update last login
            user.last_login = datetime.now()
            user.save()
            
            # Generate JWT tokens
            refresh = RefreshToken()
            refresh['user_id'] = str(user.id)
            refresh['username'] = user.username
            
            return Response({
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_active': user.is_active,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            print(f"DEBUG: Invalid password for user '{username}'")  # Debug log
            return Response({
                'error': 'Invalid password. Please check your password.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to logout
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                # If no refresh token provided, just return success
                # Frontend will clear localStorage anyway
                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            
            # Add token to blacklist using our MongoDB model
            BlacklistedToken.blacklist_token(refresh_token)
            
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Even if token blacklisting fails, consider logout successful
            # since the frontend will clear the tokens anyway
            print(f"DEBUG: Logout token blacklist failed: {e}")
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Get user profile"""
    try:
        # Extract user ID from JWT token
        user_id = request.user.id if hasattr(request.user, 'id') else None
        
        if not user_id:
            return Response({
                'error': 'User ID not found in token'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects(id=user_id).first()
        if not user:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'bio': user.bio,
                'favorite_genres': user.favorite_genres,
                'date_joined': user.date_joined.isoformat() if user.date_joined else None,
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"DEBUG: Profile view error: {e}")
        return Response({
            'error': 'Failed to fetch profile'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'database': 'MongoDB',
        'timestamp': datetime.now().isoformat()
    }, status=status.HTTP_200_OK)
