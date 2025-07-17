import React, { createContext, useContext, useState, useEffect } from 'react';
import apiService from '../services/api';

const WatchlistContext = createContext();

export const useWatchlist = () => {
  const context = useContext(WatchlistContext);
  if (!context) {
    throw new Error('useWatchlist must be used within a WatchlistProvider');
  }
  return context;
};

export const WatchlistProvider = ({ children }) => {
  const [watchlist, setWatchlist] = useState([]);
  const [watchlistStats, setWatchlistStats] = useState({
    want_to_watch: 0,
    watched: 0,
    total_watch_time: 0,
    favorite_genres: [],
    recent_activity: []
  });
  const [isLoading, setIsLoading] = useState(false);

  // Load watchlist when user is authenticated
  const loadWatchlist = async () => {
    if (!apiService.isAuthenticated()) return;
    
    setIsLoading(true);
    try {
      const data = await apiService.getWatchlist();
      setWatchlist(data.watchlist || []);
      
      // Load stats (but don't use total_movies from here since we calculate it from watchlist)
      const stats = await apiService.getWatchlistStats();
      setWatchlistStats({
        want_to_watch: stats.want_to_watch || 0,
        watched: stats.watched || 0,
        total_watch_time: stats.total_watch_time || 0,
        favorite_genres: stats.favorite_genres || [],
        recent_activity: stats.recent_activity || []
      });
    } catch (error) {
      console.error('Failed to load watchlist:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Add movie to watchlist
  const addToWatchlist = async (movie) => {
    if (!apiService.isAuthenticated()) {
      throw new Error('Please login to add movies to your watchlist');
    }

    try {
      const result = await apiService.addToWatchlist(movie);
      
      // Only update local state after successful API call
      const newItem = {
        id: result.id,
        movie_id: movie.id,
        movie_title: movie.title,
        movie_poster: movie.poster_path,
        movie_overview: movie.overview,
        movie_release_date: movie.release_date,
        movie_rating: movie.vote_average,
        date_added: new Date().toISOString()
      };
      
      setWatchlist(prev => [...prev, newItem]);
      
      return result;
    } catch (error) {
      console.error('Failed to add to watchlist:', error);
      throw error;
    }
  };

  // Remove movie from watchlist
  const removeFromWatchlist = async (movieId) => {
    try {
      await apiService.removeFromWatchlist(movieId);
      
      // Only update local state after successful API call
      setWatchlist(prev => prev.filter(item => item.movie_id !== movieId));
    } catch (error) {
      console.error('Failed to remove from watchlist:', error);
      throw error;
    }
  };

  // Clear watchlist (for logout)
  const clearWatchlist = () => {
    setWatchlist([]);
    setWatchlistStats({
      want_to_watch: 0,
      watched: 0,
      total_watch_time: 0,
      favorite_genres: [],
      recent_activity: []
    });
  };

  // Check if movie is in watchlist
  const isInWatchlist = (movieId) => {
    return watchlist.some(item => item.movie_id === movieId);
  };

  // Get watchlist item by movie ID
  const getWatchlistItem = (movieId) => {
    return watchlist.find(item => item.movie_id === movieId);
  };

  // Load watchlist on mount if authenticated
  useEffect(() => {
    if (apiService.isAuthenticated()) {
      loadWatchlist();
    }
  }, []);

  const value = {
    watchlist,
    watchlistStats: {
      ...watchlistStats,
      total_movies: watchlist.length  // Always calculate from actual watchlist
    },
    isLoading,
    loadWatchlist,
    addToWatchlist,
    removeFromWatchlist,
    isInWatchlist,
    getWatchlistItem,
    clearWatchlist
  };

  return (
    <WatchlistContext.Provider value={value}>
      {children}
    </WatchlistContext.Provider>
  );
};

export default WatchlistContext;
