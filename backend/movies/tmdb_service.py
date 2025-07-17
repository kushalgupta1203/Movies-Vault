"""
TMDB API Service
Handles all communication with The Movie Database API
"""
import requests
from django.conf import settings
import json

class TMDBService:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = "https://image.tmdb.org/t/p/"
        
    def _make_request(self, endpoint, params=None):
        """Make a request to TMDB API"""
        if not self.api_key:
            raise ValueError("TMDB API key not configured")
        
        url = f"{self.base_url}/{endpoint}"
        default_params = {'api_key': self.api_key}
        
        if params:
            default_params.update(params)
        
        try:
            response = requests.get(url, params=default_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"TMDB API Error: {e}")
            return None
    
    def search_movies(self, query, page=1):
        """Search for movies"""
        return self._make_request('search/movie', {
            'query': query,
            'page': page,
            'include_adult': False
        })
    
    def get_trending_movies(self, time_window='day', page=1):
        """Get trending movies (day or week)"""
        return self._make_request(f'trending/movie/{time_window}', {'page': page})
    
    def get_popular_movies(self, page=1):
        """Get popular movies"""
        return self._make_request('movie/popular', {'page': page})
    
    def get_top_rated_movies(self, page=1):
        """Get top rated movies"""
        return self._make_request('movie/top_rated', {'page': page})
    
    def get_now_playing_movies(self, page=1):
        """Get now playing movies"""
        return self._make_request('movie/now_playing', {'page': page})
    
    def get_upcoming_movies(self, page=1):
        """Get upcoming movies"""
        return self._make_request('movie/upcoming', {'page': page})
    
    def get_movie_details(self, movie_id):
        """Get detailed information about a specific movie"""
        return self._make_request(f'movie/{movie_id}')
    
    def get_movie_credits(self, movie_id):
        """Get cast and crew for a movie"""
        return self._make_request(f'movie/{movie_id}/credits')
    
    def get_movie_videos(self, movie_id):
        """Get videos (trailers, etc.) for a movie"""
        return self._make_request(f'movie/{movie_id}/videos')
    
    def get_similar_movies(self, movie_id, page=1):
        """Get movies similar to a specific movie"""
        return self._make_request(f'movie/{movie_id}/similar', {'page': page})
    
    def get_genres(self):
        """Get list of movie genres"""
        return self._make_request('genre/movie/list')
    
    def get_movies_by_genre(self, genre_id, page=1):
        """Get movies by genre"""
        return self._make_request('discover/movie', {
            'with_genres': genre_id,
            'page': page,
            'sort_by': 'popularity.desc'
        })
    
    def get_full_image_url(self, image_path, size='w500'):
        """Convert relative image path to full URL"""
        if not image_path:
            return None
        return f"{self.image_base_url}{size}{image_path}"

# Global instance
tmdb_service = TMDBService()
