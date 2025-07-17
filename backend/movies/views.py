from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.conf import settings
from .tmdb_service import tmdb_service
import requests

class SearchMoviesView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request):
        query = request.GET.get('query', '')
        page = request.GET.get('page', 1)
        
        if not query:
            return Response({'error': 'Query parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            data = tmdb_service.search_movies(query, page)
            if data:
                # Process the results to add full image URLs
                for movie in data.get('results', []):
                    movie['poster_url'] = tmdb_service.get_full_image_url(movie.get('poster_path'))
                    movie['backdrop_url'] = tmdb_service.get_full_image_url(movie.get('backdrop_path'), 'w1280')
                
                return Response(data)
            else:
                return Response({'error': 'Failed to fetch data from TMDB'}, 
                              status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            print(f"Search movies error: {str(e)}")  # Add logging
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TrendingMoviesView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request):
        time_window = request.GET.get('time_window', 'day')  # day or week
        page = request.GET.get('page', 1)  # Add page parameter support
        
        try:
            data = tmdb_service.get_trending_movies(time_window, page)
            if data:
                # Process the results to add full image URLs
                for movie in data.get('results', []):
                    movie['poster_url'] = tmdb_service.get_full_image_url(movie.get('poster_path'))
                    movie['backdrop_url'] = tmdb_service.get_full_image_url(movie.get('backdrop_path'), 'w1280')
                
                return Response(data)
            else:
                return Response({'error': 'Failed to fetch trending movies'}, 
                              status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PopularMoviesView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request):
        page = request.GET.get('page', 1)
        
        try:
            data = tmdb_service.get_popular_movies(page)
            if data:
                # Process the results to add full image URLs
                for movie in data.get('results', []):
                    movie['poster_url'] = tmdb_service.get_full_image_url(movie.get('poster_path'))
                    movie['backdrop_url'] = tmdb_service.get_full_image_url(movie.get('backdrop_path'), 'w1280')
                
                return Response(data)
            else:
                return Response({'error': 'Failed to fetch popular movies'}, 
                              status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TopRatedMoviesView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request):
        page = request.GET.get('page', 1)
        
        try:
            data = tmdb_service.get_top_rated_movies(page)
            if data:
                # Process the results to add full image URLs
                for movie in data.get('results', []):
                    movie['poster_url'] = tmdb_service.get_full_image_url(movie.get('poster_path'))
                    movie['backdrop_url'] = tmdb_service.get_full_image_url(movie.get('backdrop_path'), 'w1280')
                
                return Response(data)
            else:
                return Response({'error': 'Failed to fetch top rated movies'}, 
                              status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NowPlayingMoviesView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request):
        page = request.GET.get('page', 1)
        
        try:
            data = tmdb_service.get_now_playing_movies(page)
            if data:
                # Process the results to add full image URLs
                for movie in data.get('results', []):
                    movie['poster_url'] = tmdb_service.get_full_image_url(movie.get('poster_path'))
                    movie['backdrop_url'] = tmdb_service.get_full_image_url(movie.get('backdrop_path'), 'w1280')
                
                return Response(data)
            else:
                return Response({'error': 'Failed to fetch now playing movies'}, 
                              status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpcomingMoviesView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request):
        page = request.GET.get('page', 1)
        
        try:
            data = tmdb_service.get_upcoming_movies(page)
            if data:
                # Process the results to add full image URLs
                for movie in data.get('results', []):
                    movie['poster_url'] = tmdb_service.get_full_image_url(movie.get('poster_path'))
                    movie['backdrop_url'] = tmdb_service.get_full_image_url(movie.get('backdrop_path'), 'w1280')
                
                return Response(data)
            else:
                return Response({'error': 'Failed to fetch upcoming movies'}, 
                              status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieDetailView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request, movie_id):
        try:
            data = tmdb_service.get_movie_details(movie_id)
            if data:
                # Add full image URLs
                data['poster_url'] = tmdb_service.get_full_image_url(data.get('poster_path'))
                data['backdrop_url'] = tmdb_service.get_full_image_url(data.get('backdrop_path'), 'w1280')
                
                return Response(data)
            else:
                return Response({'error': 'Movie not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieCreditsView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request, movie_id):
        try:
            data = tmdb_service.get_movie_credits(movie_id)
            if data:
                # Add full image URLs for cast profiles
                for cast_member in data.get('cast', []):
                    cast_member['profile_url'] = tmdb_service.get_full_image_url(cast_member.get('profile_path'))
                
                for crew_member in data.get('crew', []):
                    crew_member['profile_url'] = tmdb_service.get_full_image_url(crew_member.get('profile_path'))
                
                return Response(data)
            else:
                return Response({'error': 'Credits not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieVideosView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request, movie_id):
        try:
            data = tmdb_service.get_movie_videos(movie_id)
            if data:
                return Response(data)
            else:
                return Response({'error': 'Videos not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SimilarMoviesView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request, movie_id):
        page = request.GET.get('page', 1)
        
        try:
            data = tmdb_service.get_similar_movies(movie_id, page)
            if data:
                # Process the results to add full image URLs
                for movie in data.get('results', []):
                    movie['poster_url'] = tmdb_service.get_full_image_url(movie.get('poster_path'))
                    movie['backdrop_url'] = tmdb_service.get_full_image_url(movie.get('backdrop_path'), 'w1280')
                
                return Response(data)
            else:
                return Response({'error': 'Similar movies not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenresView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request):
        try:
            data = tmdb_service.get_genres()
            if data:
                return Response(data)
            else:
                return Response({'error': 'Failed to fetch genres'}, 
                              status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MoviesByGenreView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow all for testing
    
    def get(self, request, genre_id):
        page = request.GET.get('page', 1)
        
        try:
            data = tmdb_service.get_movies_by_genre(genre_id, page)
            if data:
                # Process the results to add full image URLs
                for movie in data.get('results', []):
                    movie['poster_url'] = tmdb_service.get_full_image_url(movie.get('poster_path'))
                    movie['backdrop_url'] = tmdb_service.get_full_image_url(movie.get('backdrop_path'), 'w1280')
                
                return Response(data)
            else:
                return Response({'error': 'Failed to fetch movies by genre'}, 
                              status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
