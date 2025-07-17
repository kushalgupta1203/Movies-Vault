#!/usr/bin/env python3
"""
MongoDB Integration Test using MongoEngine
==========================================

This script tests the MongoDB connection and basic operations using MongoEngine
instead of djongo for better compatibility.
"""


import os
import sys
from datetime import datetime, timezone, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_vault.settings')

# Setup Django
import django
django.setup()

def test_mongodb_connection():
    """Test basic MongoDB connection"""
    print("1. Testing MongoDB Connection...")
    
    try:
        import mongoengine
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        # Get MongoDB URI
        mongodb_uri = os.getenv('MONGODB_URI')
        mongodb_db = os.getenv('MONGODB_DB_NAME', 'movies_vault')
        
        if not mongodb_uri:
            print("❌ MONGODB_URI not found in .env file")
            return False
        
        print(f"   📡 Connecting to MongoDB: {mongodb_db}")
        
        # Connect to MongoDB
        mongoengine.connect(
            db=mongodb_db,
            host=mongodb_uri,
            retryWrites=True,
            w='majority'
        )
        
        print("✅ MongoDB connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def test_user_operations():
    """Test user creation and operations"""
    print("\n2. Testing User Operations...")
    
    try:
        from authentication.mongo_models import User
        
        # Create test user
        test_username = f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        user = User(
            username=test_username,
            email=f"{test_username}@example.com",
            first_name="Test",
            last_name="User",
            bio="Test user for MongoDB integration"
        )
        user.set_password("testpassword123")
        user.save()
        
        print(f"✅ Created user: {user.username}")
        
        # Test password verification
        if user.check_password("testpassword123"):
            print("✅ Password verification works")
        else:
            print("❌ Password verification failed")
            return False
        
        # Test user query
        found_user = User.objects(username=test_username).first()
        if found_user:
            print("✅ User query successful")
        else:
            print("❌ User query failed")
            return False
        
        # Test user update
        found_user.bio = "Updated bio"
        found_user.save()
        print("✅ User update successful")
        
        # Cleanup - delete test user
        found_user.delete()
        print("✅ User deletion successful")
        
        return True
        
    except Exception as e:
        print(f"❌ User operations failed: {e}")
        return False

def test_watchlist_operations():
    """Test watchlist operations"""
    print("\n3. Testing Watchlist Operations...")
    
    try:
        from authentication.mongo_models import WatchlistItem
        
        # Create test watchlist item
        watchlist_item = WatchlistItem(
            user_id="test_user_123",
            movie_id="550",  # Fight Club
            movie_title="Fight Club",
            movie_overview="A test movie for integration testing",
            movie_release_date="1999-10-15",
            movie_rating=8.8
        )
        watchlist_item.save()
        
        print("✅ Created watchlist item")
        
        # Test query
        found_item = WatchlistItem.objects(user_id="test_user_123").first()
        if found_item:
            print("✅ Watchlist query successful")
        else:
            print("❌ Watchlist query failed")
            return False
        
        # Test update
        found_item.is_watched = True
        found_item.user_rating = 9.0
        found_item.save()
        print("✅ Watchlist update successful")
        
        # Cleanup
        found_item.delete()
        print("✅ Watchlist deletion successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Watchlist operations failed: {e}")
        return False

def test_token_blacklist():
    """Test token blacklist operations"""
    print("\n4. Testing Token Blacklist...")
    
    try:
        from authentication.mongo_models import BlacklistedToken
        
        # Test token blacklisting
        test_token = "test_jwt_token_12345"
        
        blacklisted, created = BlacklistedToken.blacklist_token(test_token)
        if created:
            print("✅ Token blacklisted successfully")
        else:
            print("❌ Token blacklisting failed")
            return False
        
        # Test blacklist check
        if BlacklistedToken.is_blacklisted(test_token):
            print("✅ Token blacklist check works")
        else:
            print("❌ Token blacklist check failed")
            return False
        
        # Cleanup
        BlacklistedToken.objects(token=test_token).delete()
        print("✅ Token cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Token blacklist operations failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 MONGODB INTEGRATION TESTS (MongoEngine)")
    print("=" * 60)
    print()
    
    # Run tests
    tests = [
        test_mongodb_connection,
        test_user_operations,
        test_watchlist_operations,
        test_token_blacklist
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            break  # Stop on first failure
    
    print()
    print("=" * 60)
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ MongoDB integration is working correctly")
        print()
        print("📋 NEXT STEPS:")
        print("1. Update your views to use MongoEngine models")
        print("2. Test authentication endpoints")
        print("3. Start the Django server: python manage.py runserver 8000")
        print("4. Test frontend integration")
    else:
        print(f"❌ TESTS FAILED: {passed}/{total} passed")
        print("Please check your MongoDB configuration and try again")
    print("=" * 60)

if __name__ == "__main__":
    main()
