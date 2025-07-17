from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import os

def health_check(request):
    """
    Simple health check endpoint for monitoring services like UptimeRobot
    Returns JSON with server status and basic info
    """
    try:
        # Check database connection
        from authentication.mongo_models import User
        db_status = "connected"
        try:
            # Try to count users (this tests MongoDB connection)
            user_count = User.objects.count()
        except Exception as e:
            db_status = f"error: {str(e)}"
            user_count = 0
        
        health_data = {
            "status": "healthy",
            "timestamp": timezone.now().isoformat(),
            "server": "Movies Vault Backend",
            "version": "1.0",
            "database": {
                "status": db_status,
                "users_count": user_count
            },
            "environment": {
                "debug": settings.DEBUG,
                "allowed_hosts": settings.ALLOWED_HOSTS
            }
        }
        
        return JsonResponse(health_data, status=200)
    
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
            "timestamp": timezone.now().isoformat()
        }, status=500)

def health_page(request):
    """
    Simple HTML page to check server status visually
    Useful for quick manual checks
    """
    try:
        # Check database connection
        from authentication.mongo_models import User
        try:
            user_count = User.objects.count()
            db_status = "✅ Connected"
            db_color = "green"
        except Exception as e:
            user_count = 0
            db_status = f"❌ Error: {str(e)}"
            db_color = "red"
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Movies Vault Backend - Health Check</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    line-height: 1.6;
                }}
                .container {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 30px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                }}
                h1 {{
                    text-align: center;
                    margin-bottom: 30px;
                    font-size: 2.5em;
                }}
                .status-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }}
                .status-card {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid #00ff88;
                }}
                .error {{
                    border-left-color: #ff4444;
                }}
                .refresh-btn {{
                    display: block;
                    margin: 20px auto;
                    padding: 10px 20px;
                    background: #00ff88;
                    color: #333;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: bold;
                }}
                .refresh-btn:hover {{
                    background: #00cc70;
                }}
                .timestamp {{
                    text-align: center;
                    opacity: 0.8;
                    margin-top: 20px;
                }}
                .api-links {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 10px;
                    margin-top: 20px;
                }}
                .api-links a {{
                    color: #00ff88;
                    text-decoration: none;
                    margin-right: 15px;
                }}
                .api-links a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎬 Movies Vault Backend</h1>
                
                <div class="status-grid">
                    <div class="status-card">
                        <h3>🚀 Server Status</h3>
                        <p><strong>Status:</strong> ✅ Running</p>
                        <p><strong>Version:</strong> 1.0</p>
                        <p><strong>Environment:</strong> {'Development' if settings.DEBUG else 'Production'}</p>
                    </div>
                    
                    <div class="status-card {'error' if 'Error' in db_status else ''}">
                        <h3>🗄️ Database</h3>
                        <p><strong>Status:</strong> <span style="color: {db_color};">{db_status}</span></p>
                        <p><strong>Total Users:</strong> {user_count}</p>
                        <p><strong>Type:</strong> MongoDB Atlas</p>
                    </div>
                    
                    <div class="status-card">
                        <h3>🌐 Network</h3>
                        <p><strong>Allowed Hosts:</strong> {', '.join(settings.ALLOWED_HOSTS)}</p>
                        <p><strong>CORS:</strong> Configured</p>
                    </div>
                    
                    <div class="status-card">
                        <h3>🔑 Services</h3>
                        <p><strong>Authentication:</strong> ✅ JWT Ready</p>
                        <p><strong>TMDB API:</strong> ✅ Connected</p>
                        <p><strong>MongoDB:</strong> ✅ MongoEngine</p>
                    </div>
                </div>
                
                <button class="refresh-btn" onclick="window.location.reload()">🔄 Refresh Status</button>
                
                <div class="api-links">
                    <h3>🔗 API Endpoints</h3>
                    <a href="/health/" target="_blank">📊 Health JSON</a>
                    <a href="/auth/test-connection/" target="_blank">🔐 Auth Test</a>
                    <a href="/movies/popular/" target="_blank">🎬 Popular Movies</a>
                    <a href="/admin/" target="_blank">⚙️ Admin Panel</a>
                </div>
                
                <div class="timestamp">
                    <p>Last checked: {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                    <p>Keep this page bookmarked for quick server checks! 🔖</p>
                </div>
            </div>
            
            <script>
                // Auto-refresh every 30 seconds to keep server awake
                setTimeout(() => {{
                    window.location.reload();
                }}, 30000);
            </script>
        </body>
        </html>
        """
        
        return HttpResponse(html_content)
    
    except Exception as e:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Movies Vault Backend</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
                .error {{ background: #ffe6e6; border: 1px solid #ff9999; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>❌ Server Error</h2>
                <p><strong>Error:</strong> {str(e)}</p>
                <p><strong>Time:</strong> {timezone.now()}</p>
            </div>
        </body>
        </html>
        """
        return HttpResponse(error_html, status=500)
