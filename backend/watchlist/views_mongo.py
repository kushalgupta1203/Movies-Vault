from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.mongo_models import User, WatchlistItem, UserMovieInteraction
from movies.tmdb_service import tmdb_service
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

def get_user_from_token(request):
    """Extract user from JWT token"""
    try:
        # Get the wrapped user from our custom authentication
        if hasattr(request.user, 'mongo_user'):
            # User authenticated through our custom MongoJWTAuthentication
            return request.user.mongo_user
        elif hasattr(request.user, 'id') and request.user.id:
            # Try to get user by ID from MongoDB
            from authentication.mongo_models import User
            return User.objects(id=request.user.id).first()
        return None
    except Exception as e:
        logger.error(f"Error getting user from token: {e}")
        return None

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    """Get user's watchlist with optional filtering"""
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        watchlist_items = WatchlistItem.objects(user_id=str(user.id))
        
        # Filter by watch status if provided
        status_filter = request.GET.get('status')
        if status_filter == 'watched':
            watchlist_items = watchlist_items.filter(is_watched=True)
        elif status_filter == 'want_to_watch':
            watchlist_items = watchlist_items.filter(is_watched=False)
        
        # Convert to serializable format
        watchlist_data = []
        for item in watchlist_items:
            watchlist_data.append({
                'id': str(item.id),
                'movie_id': item.movie_id,
                'movie_title': item.movie_title,
                'movie_poster': item.movie_poster,
                'movie_overview': item.movie_overview,
                'movie_release_date': item.movie_release_date,
                'movie_rating': item.movie_rating,
                'is_watched': item.is_watched,
                'user_rating': item.user_rating,
                'user_review': item.user_review,
                'date_added': item.date_added.isoformat() if item.date_added else None,
                'date_watched': item.date_watched.isoformat() if item.date_watched else None,
            })
        
        return Response({
            'watchlist': watchlist_data,
            'count': len(watchlist_data)
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Get watchlist error: {str(e)}")
        return Response({
            'error': 'Failed to get watchlist'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_watchlist(request):
    """Add movie to user's watchlist"""
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({
                'error': 'Movie ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already in watchlist
        existing_item = WatchlistItem.objects(user_id=str(user.id), movie_id=str(movie_id)).first()
        if existing_item:
            return Response({
                'error': 'Movie is already in your watchlist'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch movie details from TMDB
        movie_details = tmdb_service.get_movie_details(movie_id)
        if not movie_details:
            return Response({
                'error': 'Movie not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Create watchlist item
        watchlist_item = WatchlistItem(
            user_id=str(user.id),
            movie_id=str(movie_id),
            movie_title=movie_details.get('title', ''),
            movie_poster=f"https://image.tmdb.org/t/p/w500{movie_details.get('poster_path', '')}" if movie_details.get('poster_path') else '',
            movie_overview=movie_details.get('overview', ''),
            movie_release_date=movie_details.get('release_date', ''),
            movie_rating=movie_details.get('vote_average', 0)
        )
        watchlist_item.save()
        
        return Response({
            'message': 'Movie added to watchlist successfully',
            'watchlist_item': {
                'id': str(watchlist_item.id),
                'movie_id': watchlist_item.movie_id,
                'movie_title': watchlist_item.movie_title,
                'movie_poster': watchlist_item.movie_poster,
                'date_added': watchlist_item.date_added.isoformat(),
            }
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        logger.error(f"Add to watchlist error: {str(e)}")
        return Response({
            'error': 'Failed to add movie to watchlist'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_watchlist(request, movie_id):
    """Remove movie from user's watchlist"""
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        watchlist_item = WatchlistItem.objects(user_id=str(user.id), movie_id=str(movie_id)).first()
        if not watchlist_item:
            return Response({
                'error': 'Movie not found in watchlist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        watchlist_item.delete()
        
        return Response({
            'message': 'Movie removed from watchlist successfully'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Remove from watchlist error: {str(e)}")
        return Response({
            'error': 'Failed to remove movie from watchlist'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_as_watched(request, movie_id):
    """Mark movie as watched"""
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        watchlist_item = WatchlistItem.objects(user_id=str(user.id), movie_id=str(movie_id)).first()
        if not watchlist_item:
            return Response({
                'error': 'Movie not found in watchlist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        watchlist_item.is_watched = True
        watchlist_item.date_watched = datetime.now()
        
        # Optional: Add user rating and review
        user_rating = request.data.get('rating')
        if user_rating:
            watchlist_item.user_rating = float(user_rating)
        
        user_review = request.data.get('review')
        if user_review:
            watchlist_item.user_review = user_review
        
        watchlist_item.save()
        
        return Response({
            'message': 'Movie marked as watched',
            'watchlist_item': {
                'id': str(watchlist_item.id),
                'movie_id': watchlist_item.movie_id,
                'is_watched': watchlist_item.is_watched,
                'date_watched': watchlist_item.date_watched.isoformat(),
                'user_rating': watchlist_item.user_rating,
                'user_review': watchlist_item.user_review,
            }
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Mark as watched error: {str(e)}")
        return Response({
            'error': 'Failed to mark movie as watched'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_watchlist_status(request, movie_id):
    """Check if movie is in user's watchlist"""
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        watchlist_item = WatchlistItem.objects(user_id=str(user.id), movie_id=str(movie_id)).first()
        
        return Response({
            'in_watchlist': watchlist_item is not None,
            'is_watched': watchlist_item.is_watched if watchlist_item else False
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Check watchlist status error: {str(e)}")
        return Response({
            'error': 'Failed to check watchlist status'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
