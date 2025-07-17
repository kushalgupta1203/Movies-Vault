from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import User, UserPreferences
from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer, 
    UserLoginSerializer,
    UserPreferencesSerializer
)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Check if username already exists
        username = request.data.get('username')
        if not username:
            return Response({
                'error': 'Username is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(username=username).exists():
            print(f"DEBUG: Username '{username}' already exists")  # Debug log
            return Response({
                'error': 'Username already exists. Please choose a different username.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
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
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.password = make_password(serializer.validated_data['password'])
            user.save()
            
            # Create user preferences
            UserPreferences.objects.create(user=user)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        
        # Handle validation errors
        errors = []
        for field, error_list in serializer.errors.items():
            for error in error_list:
                errors.append(f"{field}: {error}")
        
        return Response({
            'error': '; '.join(errors) if errors else 'Registration failed'
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
        try:
            user_exists = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"DEBUG: User '{username}' does not exist")  # Debug log
            return Response({
                'error': 'Username does not exist. Please check your username or sign up.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if account is active
        if not user_exists.is_active:
            print(f"DEBUG: User '{username}' account is disabled")  # Debug log
            return Response({
                'error': 'Your account has been disabled. Please contact support.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user:
            print(f"DEBUG: User '{username}' authenticated successfully")  # Debug log
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
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
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Even if token blacklisting fails, consider logout successful
            # since the frontend will clear the tokens anyway
            print(f"DEBUG: Logout token blacklist failed: {e}")
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestLoginView(APIView):
    """
    Temporary test login view that bypasses authentication
    FOR TESTING PURPOSES ONLY - REMOVE IN PRODUCTION
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Return mock successful login for any credentials during testing
        return Response({
            'user': {
                'id': 1,
                'username': 'testuser',
                'email': 'test@moviesvault.com',
                'first_name': 'Test',
                'last_name': 'User'
            },
            'access': 'mock_access_token',
            'refresh': 'mock_refresh_token',
            'message': 'Test login successful'
        }, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.password = make_password(new_password)
        user.save()
        
        return Response({'message': 'Password changed successfully'})
