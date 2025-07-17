from django.db import models
from django.conf import settings
from django.utils import timezone

class WatchlistItem(models.Model):
    """Movies in user's watchlist with watch status - MongoDB Compatible"""
    
    WATCH_STATUS_CHOICES = [
        ('want_to_watch', 'Want to Watch'),
        ('watched', 'Watched'),
    ]
    
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist')
    movie_id = models.IntegerField()  # TMDB movie ID
    movie_title = models.CharField(max_length=255)
    movie_poster = models.URLField(max_length=500, null=True, blank=True)
    movie_overview = models.TextField(blank=True)
    movie_release_date = models.DateField(null=True, blank=True)
    movie_rating = models.FloatField(null=True, blank=True)  # TMDB rating
    
    # Watch status - the key feature you requested
    watch_status = models.CharField(max_length=20, choices=WATCH_STATUS_CHOICES, default='want_to_watch')
    user_rating = models.IntegerField(null=True, blank=True)  # User's personal rating (1-10)
    notes = models.TextField(blank=True)
    
    # Timestamps
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    watched_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'watchlist_items'
    
    def __str__(self):
        return f"{self.user.username} - {self.movie_title} ({self.watch_status})"
    
    def mark_as_watched(self):
        """Mark movie as watched"""
        self.watch_status = 'watched'
        self.watched_at = timezone.now()
        self.save()
    
    def mark_as_want_to_watch(self):
        """Mark movie as want to watch"""
        self.watch_status = 'want_to_watch'
        self.watched_at = None
        self.save()

class UserMovieInteraction(models.Model):
    """Track user interactions for analytics - MongoDB Compatible"""
    
    INTERACTION_TYPES = [
        ('view', 'Viewed'),
        ('add_to_watchlist', 'Added to Watchlist'),
        ('remove_from_watchlist', 'Removed from Watchlist'),
        ('mark_watched', 'Marked as Watched'),
        ('mark_unwatched', 'Marked as Unwatched'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    interaction_type = models.CharField(max_length=30, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_movie_interactions'
    
    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - Movie {self.movie_id}"
