from rest_framework import serializers
from .models import WatchlistItem, UserMovieInteraction

class WatchlistItemSerializer(serializers.ModelSerializer):
    """Serializer for WatchlistItem model"""
    
    class Meta:
        model = WatchlistItem
        fields = [
            'id', 'movie_id', 'movie_title', 'movie_poster', 'movie_overview',
            'movie_release_date', 'movie_rating', 'watch_status', 'user_rating',
            'notes', 'added_at', 'updated_at', 'watched_at'
        ]
        read_only_fields = ['id', 'added_at', 'updated_at']

class AddToWatchlistSerializer(serializers.Serializer):
    """Serializer for adding movies to watchlist"""
    movie_id = serializers.IntegerField()
    movie_title = serializers.CharField(max_length=255)
    movie_poster = serializers.CharField(max_length=500, required=False)
    movie_overview = serializers.CharField(required=False)
    movie_release_date = serializers.CharField(max_length=20, required=False)
    movie_rating = serializers.FloatField(required=False)
    watch_status = serializers.ChoiceField(
        choices=WatchlistItem.WATCH_STATUS_CHOICES,
        default='want_to_watch'
    )

class MarkWatchedSerializer(serializers.Serializer):
    """Serializer for marking movies as watched"""
    movie_id = serializers.IntegerField()

class UserMovieInteractionSerializer(serializers.ModelSerializer):
    """Serializer for UserMovieInteraction model"""
    
    class Meta:
        model = UserMovieInteraction
        fields = ['id', 'movie_id', 'interaction_type', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class WatchlistStatsSerializer(serializers.Serializer):
    """Serializer for watchlist statistics"""
    total_movies = serializers.IntegerField()
    want_to_watch = serializers.IntegerField()
    watched = serializers.IntegerField()
    total_watch_time = serializers.IntegerField()  # in minutes
    favorite_genres = serializers.ListField()
    recent_activity = WatchlistItemSerializer(many=True)

