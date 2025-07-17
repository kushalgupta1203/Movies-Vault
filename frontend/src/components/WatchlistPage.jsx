import React, { useEffect, useState } from 'react';
import { useWatchlist } from '../context/WatchlistContext';
import { useAuth } from '../context/AuthContext';
import Spinner from './Spinner';

// Watchlist Movie Card Component
const WatchlistMovieCard = ({ item, onRemove }) => {
  const getPosterUrl = (posterPath) => {
    if (!posterPath) return '/no-movie.png';
    if (posterPath.startsWith('http')) return posterPath;
    return `https://image.tmdb.org/t/p/w500${posterPath}`;
  };

  // Function to format date properly
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return 'Recently added';
      }
      return date.toLocaleDateString();
    } catch (error) {
      return 'Recently added';
    }
  };

  return (
    <div className="movie-card watchlist-movie-card">
      <div className="movie-poster-container">
        <img
          src={getPosterUrl(item.movie_poster)}
          alt={item.movie_title}
        />
        
        {/* Remove Button - positioned like the plus button */}
        <button 
          className="watchlist-btn remove-btn" 
          onClick={onRemove}
          title="Remove from Watchlist"
        >
          ✕
        </button>
      </div>

      <div className="mt-4">
        <h3>{item.movie_title}</h3>

        <div className="content">
          <div className="rating">
            <img src="/star.svg" alt="Star Icon" />
            <p>{item.movie_rating ? item.movie_rating.toFixed(1) : 'N/A'}</p>
          </div>

          <span>•</span>
          <p className="year">
            {item.movie_release_date ? item.movie_release_date.split('-')[0] : 'N/A'}
          </p>
        </div>
        
        <div className="date-added">
          Added: {formatDate(item.date_added)}
        </div>
      </div>
    </div>
  );
};

const WatchlistPage = () => {
  const { isAuthenticated } = useAuth();
  const { 
    watchlist, 
    watchlistStats, 
    isLoading, 
    loadWatchlist, 
    removeFromWatchlist
  } = useWatchlist();

  useEffect(() => {
    if (isAuthenticated) {
      loadWatchlist();
    }
  }, [isAuthenticated]);

  const handleRemoveFromWatchlist = async (movieId) => {
    try {
      await removeFromWatchlist(movieId);
    } catch (error) {
      alert(error.message || 'Failed to remove from watchlist');
    }
  };

  const getPosterUrl = (posterPath) => {
    if (!posterPath) return '/no-movie.png';
    if (posterPath.startsWith('http')) return posterPath;
    return `https://image.tmdb.org/t/p/w500${posterPath}`;
  };

  if (!isAuthenticated) {
    return (
      <div className="watchlist-page">
        <div className="watchlist-empty">
          <h2>Please login to view your watchlist</h2>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="watchlist-page">
        <Spinner />
      </div>
    );
  }

  return (
    <div className="watchlist-page">
      {/* Watchlist Content */}
      {watchlist.length === 0 ? (
        <div className="watchlist-empty">
          <h2>Your watchlist is empty</h2>
          <p>Start adding movies to your watchlist by clicking the + button on any movie card</p>
        </div>
      ) : (
        <>
          {/* Watchlist Stats - only show when there are movies */}
          <div className="watchlist-stats">
            <div className="stats-grid">
              <div className="stat-item">
                <p style={{ color: 'white', fontWeight: 'bold', fontSize: '18px', margin: 0 }}>
                  Total movies in watchlist: {watchlistStats.total_movies}
                </p>
              </div>
            </div>
          </div>

          <section className="all-movies">
            <ul className="watchlist-movies-grid">
              {watchlist.map(item => (
                <WatchlistMovieCard 
                  key={item.id} 
                  item={item}
                  onRemove={() => handleRemoveFromWatchlist(item.movie_id)}
                />
              ))}
            </ul>
          </section>
        </>
      )}
    </div>
  );
};

export default WatchlistPage;
