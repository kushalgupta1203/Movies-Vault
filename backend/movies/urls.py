from django.urls import path
from . import views


urlpatterns = [
    # Movie search and discovery
    path('search/', views.SearchMoviesView.as_view(), name='search_movies'),
    path('trending/', views.TrendingMoviesView.as_view(), name='trending_movies'),
    path('popular/', views.PopularMoviesView.as_view(), name='popular_movies'),
    path('top-rated/', views.TopRatedMoviesView.as_view(), name='top_rated_movies'),
    path('now-playing/', views.NowPlayingMoviesView.as_view(), name='now_playing_movies'),
    path('upcoming/', views.UpcomingMoviesView.as_view(), name='upcoming_movies'),
    
    # Movie details
    path('<int:movie_id>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('<int:movie_id>/credits/', views.MovieCreditsView.as_view(), name='movie_credits'),
    path('<int:movie_id>/videos/', views.MovieVideosView.as_view(), name='movie_videos'),
    path('<int:movie_id>/similar/', views.SimilarMoviesView.as_view(), name='similar_movies'),
    
    # Genre endpoints
    path('genres/', views.GenresView.as_view(), name='genres'),
    path('genres/<int:genre_id>/', views.MoviesByGenreView.as_view(), name='movies_by_genre'),
]
