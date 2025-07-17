import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useWatchlist } from '../context/WatchlistContext';

const MovieCard = ({ movie:
  { id, title, vote_average, poster_path, release_date, original_language, overview }
}) => {
  const { isAuthenticated } = useAuth();
  const { addToWatchlist, removeFromWatchlist, isInWatchlist } = useWatchlist();
  const [isLoading, setIsLoading] = useState(false);

  // Handle poster URL - check if it's already a full URL or needs to be constructed
  const getPosterUrl = () => {
    if (!poster_path) return '/no-movie.png';
    
    // If it's already a full URL, use it as is
    if (poster_path.startsWith('http')) return poster_path;
    
    // Otherwise, construct the full TMDB URL
    return `https://image.tmdb.org/t/p/w500${poster_path}`;
  };

  // Handle watchlist button click
  const handleWatchlistClick = async (e) => {
    e.stopPropagation(); // Prevent any parent click handlers
    
    if (!isAuthenticated) {
      alert('Please login to add movies to your watchlist');
      return;
    }

    setIsLoading(true);
    try {
      const movieData = {
        id,
        title,
        poster_path,
        overview,
        release_date,
        vote_average
      };

      if (isInWatchlist(id)) {
        await removeFromWatchlist(id);
      } else {
        await addToWatchlist(movieData);
      }
    } catch (error) {
      console.error('Watchlist operation failed:', error);
      alert(error.message || 'Failed to update watchlist');
    } finally {
      setIsLoading(false);
    }
  };

  const inWatchlist = isInWatchlist(id);

  return (
    <div className="movie-card">
      <div className="movie-poster-container">
        <img
          src={getPosterUrl()}
          alt={title}
        />
        <button 
          className={`watchlist-btn ${inWatchlist ? 'added' : ''}`}
          title={inWatchlist ? 'Remove from Watchlist' : 'Add to Watchlist'}
          onClick={handleWatchlistClick}
          disabled={isLoading}
        >
          {isLoading ? '...' : inWatchlist ? '✓' : '+'}
        </button>
      </div>

      <div className="mt-4">
        <h3>{title}</h3>

        <div className="content">
          <div className="rating">
            <img src="star.svg" alt="Star Icon" />
            <p>{vote_average ? vote_average.toFixed(1) : 'N/A'}</p>
          </div>

          <span>•</span>
          <p className="lang">{original_language}</p>

          <span>•</span>
          <p className="year">
            {release_date ? release_date.split('-')[0] : 'N/A'}
          </p>
        </div>
      </div>
    </div>
  )
}

export default MovieCard;
