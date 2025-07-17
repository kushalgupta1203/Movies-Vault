import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [showSignup, setShowSignup] = useState(false);
  
  const { login, register } = useAuth();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // Client-side validation
    if (formData.password.length < 8) {
      const errorMsg = 'Password must be at least 8 characters long';
      setError(errorMsg);
      alert(errorMsg); // Simple popup to ensure visibility
      setIsLoading(false);
      return;
    }

    if (formData.username.length < 3) {
      const errorMsg = 'Username must be at least 3 characters long';
      setError(errorMsg);
      alert(errorMsg); // Simple popup to ensure visibility
      setIsLoading(false);
      return;
    }

    try {
      if (showSignup) {
        // Handle registration
        await register({
          username: formData.username,
          password: formData.password
        });
      } else {
        // Handle login
        await login(formData.username, formData.password);
      }
    } catch (err) {
      // Extract error message from different possible sources
      let errorMessage = '';
      if (err.message) {
        errorMessage = err.message;
      } else if (err.error) {
        errorMessage = err.error;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else {
        errorMessage = 'An unexpected error occurred';
      }
      
      if (showSignup) {
        // SIGNUP ERROR HANDLING - Match exact backend messages and show user-friendly debug info
        if (errorMessage.includes('Username already exists')) {
          const errorMsg = `User '${formData.username}' already exists. Use different username.`;
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('Password must be at least 8 characters long')) {
          const errorMsg = 'Password must be at least 8 characters long.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('Username must be at least 3 characters long')) {
          const errorMsg = 'Username must be at least 3 characters long.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('Username is required')) {
          const errorMsg = 'Username is required.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('Password is required')) {
          const errorMsg = 'Password is required.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('This field may not be blank')) {
          const errorMsg = 'Please fill in all required fields.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('Network error')) {
          const errorMsg = 'Network error. Please check your connection and try again.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else {
          // Fallback: show the actual error message from backend
          const errorMsg = errorMessage || 'Registration failed. Please try again.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        }
      } else {
        // LOGIN ERROR HANDLING - Match exact backend messages and show user-friendly debug info
        if (errorMessage.includes('Username does not exist')) {
          const errorMsg = `User '${formData.username}' does not exist. Please check your username or sign up.`;
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('Invalid password')) {
          const errorMsg = `Invalid password for user '${formData.username}'. Please check your password.`;
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('account has been disabled')) {
          const errorMsg = `Account '${formData.username}' has been disabled. Please contact support.`;
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('Username is required')) {
          const errorMsg = 'Username is required.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('Password is required')) {
          const errorMsg = 'Password is required.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else if (errorMessage.includes('Network error')) {
          const errorMsg = 'Network error. Please check your connection and try again.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        } else {
          // Fallback: show the actual error message from backend
          const errorMsg = errorMessage || 'Login failed. Please try again.';
          setError(errorMsg);
          alert(errorMsg); // Simple popup to ensure visibility
        }
      }
    } finally {
      setIsLoading(false);
    }
  };

  const toggleForm = () => {
    setShowSignup(!showSignup);
    setError('');
    setFormData({
      username: '',
      password: ''
    });
  };

  return (
    <div className="login-container">
      {/* Background */}
      <div className="login-background"></div>

      {/* Main Content */}
      <div className="login-content">
        {/* Single wrapper for all login elements */}
        <div className="login-wrapper">
          {/* Logo */}
          <div className="login-logo">
            <img src="/logo.png" alt="Movies Vault" />
          </div>

          {/* Title */}
          <div className="login-title">
            <h1>
              <span className="movies-text">MOVIES</span><span className="vault-text">VAULT</span>
            </h1>
          </div>

          {/* Subtitle */}
          <div className="login-subtitle">
            <p className="tagline">Visual Archive for User's Liked & Tracked Movies</p>
          </div>

          {/* Login Form */}
          <div className="login-form-container">
            <form onSubmit={handleSubmit}>
              <h2>{showSignup ? 'Sign Up' : 'Login'}</h2>
            
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="username" className="form-label">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                className="form-input"
                placeholder="Enter your username"
                required
                disabled={isLoading}
                minLength="3"
              />
              {formData.username && formData.username.length < 3 && (
                <div className="input-error">Username must be at least 3 characters long</div>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="password" className="form-label">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className="form-input"
                placeholder="Enter your password"
                required
                disabled={isLoading}
                minLength="8"
              />
              {formData.password && formData.password.length < 8 && (
                <div className="input-error">Password must be at least 8 characters long</div>
              )}
            </div>

            <button 
              type="submit" 
              className="login-btn"
              disabled={isLoading}
            >
              {isLoading 
                ? (showSignup ? 'Creating Account...' : 'Signing In...') 
                : (showSignup ? 'Create Account' : 'Sign In')
              }
            </button>

            <div className="login-footer">
              <p>
                {showSignup ? 'Already have an account?' : "Don't have an account?"}{' '}
                <a href="#" onClick={(e) => { e.preventDefault(); toggleForm(); }}>
                  {showSignup ? 'Sign In' : 'Sign Up'}
                </a>
              </p>
            </div>
          </form>
        </div>
        </div>
      </div>

      {/* Server Wake-up Button - Fixed Bottom Left */}
      <div className="server-wake-fixed">
        <button 
          type="button"
          className="server-wake-btn fixed-position"
          onClick={() => window.open('https://movies-vault-backend.onrender.com/', '_blank')}
          title="Click if server is not responding (wakes up sleeping server)"
        >
          Switch On Server
        </button>
      </div>
    </div>
  );
};

export default Login;
