from django.db import models



class MovieCache(models.Model):
    """Cache for TMDB movie data to reduce API calls"""
    movie_id = models.IntegerField(unique=True)  # TMDB movie ID
    title = models.CharField(max_length=255)
    overview = models.TextField()
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    runtime = models.IntegerField(null=True, blank=True)
    genres = models.JSONField(default=list)
    production_companies = models.JSONField(default=list)
    production_countries = models.JSONField(default=list)
    spoken_languages = models.JSONField(default=list)
    adult = models.BooleanField(default=False)
    popularity = models.FloatField()
    
    # Cache metadata
    cached_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-popularity']
    
    def __str__(self):
        return self.title

class Genre(models.Model):
    """Movie genres from TMDB"""
    genre_id = models.IntegerField(unique=True)  # TMDB genre ID
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
