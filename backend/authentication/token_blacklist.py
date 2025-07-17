"""
Simple Token Blacklist Model for MongoDB
========================================

This replaces the rest_framework_simplejwt.token_blacklist functionality
with a MongoDB-compatible solution.
"""

from django.db import models
from datetime import datetime, timezone




class BlacklistedToken(models.Model):
    """
    Simple model to store blacklisted JWT tokens
    """
    token = models.TextField(unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'blacklisted_tokens'
        ordering = ['-blacklisted_at']
    
    def __str__(self):
        return f"Blacklisted token: {self.token[:20]}..."
    
    @classmethod
    def is_blacklisted(cls, token):
        """Check if a token is blacklisted"""
        return cls.objects.filter(token=token).exists()
    
    @classmethod
    def blacklist_token(cls, token, expires_at=None):
        """Add a token to the blacklist"""
        if expires_at is None:
            # Default to 7 days from now
            from datetime import timedelta
            expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        obj, created = cls.objects.get_or_create(
            token=token,
            defaults={'expires_at': expires_at}
        )
        return obj, created
    
    @classmethod
    def cleanup_expired(cls):
        """Remove expired tokens from blacklist"""
        now = datetime.now(timezone.utc)
        expired_count = cls.objects.filter(expires_at__lt=now).delete()[0]
        return expired_count


# Management command to clean up expired tokens
def cleanup_expired_tokens():
    """Function to clean up expired blacklisted tokens"""
    from .models import BlacklistedToken
    count = BlacklistedToken.cleanup_expired()
    print(f"Cleaned up {count} expired blacklisted tokens")
    return count
