# 🎬 Movies Vault

A full-stack movie discovery and watchlist management application built with React and Django.

## ✨ Features

- 🔍 **Movie Search**: Discover movies using The Movie Database (TMDB) API
- 📝 **User Authentication**: Secure JWT-based authentication with MongoDB
- 💾 **Watchlist Management**: Add and remove movies from your personal watchlist
- 🎯 **Movie Details**: View comprehensive movie information including ratings, release dates, and overviews
- 📱 **Responsive Design**: Mobile-friendly interface with modern UI
- 🔒 **Secure Backend**: MongoDB Atlas integration with custom authentication

## 🏗️ Tech Stack

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool and development server
- **CSS3** - Custom styling with responsive design
- **JavaScript ES6+** - Modern JavaScript features

### Backend
- **Django 5.1** - Python web framework
- **Django REST Framework** - API development
- **MongoEngine** - MongoDB object modeling
- **JWT Authentication** - Secure token-based auth
- **TMDB API** - Movie data integration

### Database
- **MongoDB Atlas** - Cloud-hosted MongoDB database

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- MongoDB Atlas account
- TMDB API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kushalgupta1203/Movies-Vault.git
   cd Movies-Vault
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Create .env file with your credentials
   cp .env.example .env
   # Edit .env with your MongoDB URI, TMDB API key, and Django secret
   
   python manage.py runserver 8000
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## 🔧 Environment Variables

### Backend (.env)
```env
MONGODB_URI=your_mongodb_atlas_connection_string
DJANGO_SECRET_KEY=your_django_secret_key
TMDB_API_KEY=your_tmdb_api_key
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend
Environment variables are configured in the Vite config for API endpoints.

## 📁 Project Structure

```
Movies-Vault/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── context/         # React context (Auth, Watchlist)
│   │   ├── pages/           # Page components
│   │   └── services/        # API services
│   ├── public/              # Static assets
│   └── package.json
├── backend/                 # Django application
│   ├── movies_vault/        # Django project settings
│   ├── authentication/     # User auth app
│   ├── movies/              # Movies app with TMDB integration
│   ├── watchlist/           # Watchlist management app
│   ├── core/                # Core utilities
│   └── requirements.txt
└── README.md
```

## 🌐 API Endpoints

### Authentication
- `POST /auth/register/` - User registration
- `POST /auth/login/` - User login
- `POST /auth/logout/` - User logout
- `POST /auth/refresh/` - Refresh JWT token

### Movies
- `GET /movies/search/` - Search movies
- `GET /movies/popular/` - Get popular movies
- `GET /movies/details/{id}/` - Get movie details

### Watchlist
- `GET /watchlist/` - Get user's watchlist
- `POST /watchlist/add/` - Add movie to watchlist
- `DELETE /watchlist/remove/{id}/` - Remove movie from watchlist
- `GET /watchlist/stats/` - Get watchlist statistics

## 🔐 Security Features

- JWT token-based authentication
- Password hashing with Django's built-in security
- CORS protection
- MongoDB ObjectId handling
- Environment variable protection
- Input validation and sanitization

## 🚀 Deployment

This application is designed for deployment on:
- **Frontend**: Netlify (automatic deployment from Git)
- **Backend**: Railway or Render (Python/Django support)
- **Database**: MongoDB Atlas (already configured)

### Deployment Steps
1. Push code to GitHub repository
2. Connect Netlify to frontend folder
3. Connect Railway/Render to backend folder
4. Configure environment variables on hosting platforms
5. Update CORS settings for production domains

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for movie data
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) for database hosting
- [Django](https://www.djangoproject.com/) and [React](https://reactjs.org/) communities

## 📧 Contact

Kushal Gupta - [@kushalgupta1203](https://github.com/kushalgupta1203)

Project Link: [https://github.com/kushalgupta1203/Movies-Vault](https://github.com/kushalgupta1203/Movies-Vault)

---

⭐ Don't forget to give the project a star if you found it helpful!
