"""
MongoEngine Models for Authentication - Direct MongoDB Integration
================================================================

These models use MongoEngine for direct MongoDB integration, avoiding
djongo compatibility issues.
"""

from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, ListField, FloatField, URLField
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timezone, timedelta
import json



class User(Document):
    """User model using MongoEngine for MongoDB"""
    username = StringField(required=True, unique=True, max_length=150)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    first_name = StringField(max_length=150, default='')
    last_name = StringField(max_length=150, default='')
    
    # Additional fields
    date_of_birth = DateTimeField()
    profile_picture = URLField()
    bio = StringField(max_length=500, default='')
    favorite_genres = ListField(StringField(max_length=50))
    
    # Django-compatible fields
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    date_joined = DateTimeField(default=datetime.now)
    last_login = DateTimeField()
    
    # Timestamps
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'users',
        'indexes': ['username', 'email']
    }
    
    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        """Hash and set password"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if raw password matches hashed password"""
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        """Override save to update timestamps"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)


class UserPreferences(Document):
    """User preferences for movie recommendations"""
    user_id = StringField(required=True, unique=True)  # Reference to User._id
    preferred_genres = ListField(StringField(max_length=50))
    preferred_languages = ListField(StringField(max_length=10))
    min_rating = FloatField(default=6.0)
    include_adult = BooleanField(default=False)
    
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'user_preferences',
        'indexes': ['user_id']
    }
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)


class BlacklistedToken(Document):
    """Blacklisted JWT tokens"""
    token = StringField(required=True, unique=True)
    blacklisted_at = DateTimeField(default=datetime.now)
    expires_at = DateTimeField(required=True)
    
    meta = {
        'collection': 'blacklisted_tokens',
        'indexes': ['token', 'expires_at']
    }
    
    @classmethod
    def is_blacklisted(cls, token):
        """Check if a token is blacklisted"""
        return cls.objects(token=token).first() is not None
    
    @classmethod
    def blacklist_token(cls, token, expires_at=None):
        """Add a token to the blacklist"""
        if expires_at is None:
            expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        try:
            # Try to get existing token
            existing = cls.objects(token=token).first()
            if existing:
                return existing, False
            
            # Create new blacklisted token
            blacklisted = cls(token=token, expires_at=expires_at)
            blacklisted.save()
            return blacklisted, True
        except Exception as e:
            print(f"Error blacklisting token: {e}")
            return None, False
    
    @classmethod
    def cleanup_expired(cls):
        """Remove expired tokens from blacklist"""
        now = datetime.now(timezone.utc)
        expired_tokens = cls.objects(expires_at__lt=now)
        count = expired_tokens.count()
        expired_tokens.delete()
        return count


class WatchlistItem(Document):
    """User's watchlist items"""
    user_id = StringField(required=True)
    movie_id = StringField(required=True)
    movie_title = StringField(required=True)
    movie_poster = URLField()
    movie_overview = StringField()
    movie_release_date = StringField()
    movie_rating = FloatField()
    
    # User interaction
    is_watched = BooleanField(default=False)
    user_rating = FloatField()
    user_review = StringField()
    date_added = DateTimeField(default=datetime.now)
    date_watched = DateTimeField()
    
    # Timestamps
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'watchlist_items',
        'indexes': [
            'user_id', 
            'movie_id', 
            {
                'fields': ('user_id', 'movie_id'),
                'unique': True
            }
        ]
    }
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)


class UserMovieInteraction(Document):
    """Track user interactions with movies"""
    user_id = StringField(required=True)
    movie_id = StringField(required=True)
    
    # Interaction types
    liked = BooleanField()
    rating = FloatField()
    review = StringField()
    watched_date = DateTimeField()
    
    # Timestamps
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'user_movie_interactions',
        'indexes': [
            'user_id', 
            'movie_id',
            {
                'fields': ('user_id', 'movie_id'),
                'unique': True
            }
        ]
    }
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)
