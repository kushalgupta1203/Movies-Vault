#!/usr/bin/env python3
"""
Test watchlist functionality with authenticated user
"""

import requests
import json
import time


BASE_URL = "http://127.0.0.1:8000/api"

def register_and_login():
    """Register a new user and get access token"""
    timestamp = int(time.time())
    
    registration_data = {
        "username": f"watchtest{timestamp}",
        "email": f"watchtest{timestamp}@moviesvault.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "first_name": "Watch",
        "last_name": "Tester"
    }
    
    # Register
    response = requests.post(f"{BASE_URL}/auth/register/", json=registration_data)
    if response.status_code == 201:
        data = response.json()
        return data.get('access'), registration_data['username']
    return None, None

def test_watchlist_operations():
    """Test all watchlist operations"""
    print("🎬 Movies Vault Watchlist Test")
    print("=" * 40)
    
    # Step 1: Get authentication
    print("🔐 Getting authentication...")
    access_token, username = register_and_login()
    
    if not access_token:
        print("❌ Failed to authenticate")
        return
    
    print(f"✅ Authenticated as: {username}")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Step 2: Test empty watchlist
    print("\n📋 Testing empty watchlist...")
    response = requests.get(f"{BASE_URL}/watchlist/", headers=headers)
    print(f"Empty watchlist status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Empty watchlist count: {data.get('count', 0)}")
    
    # Step 3: Add movie to watchlist
    print("\n➕ Adding movie to watchlist...")
    movie_data = {
        "movie_id": 550,  # Fight Club
        "movie_title": "Fight Club",
        "movie_poster": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "movie_overview": "A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy.",
        "movie_release_date": "1999-10-15",
        "movie_rating": 8.4
    }
    
    response = requests.post(f"{BASE_URL}/watchlist/add/", json=movie_data, headers=headers)
    print(f"Add movie status: {response.status_code}")
    if response.status_code == 201:
        print("✅ Movie added successfully!")
    else:
        print(f"❌ Failed to add movie: {response.text[:200]}")
        return
    
    # Step 4: Check watchlist again
    print("\n📋 Checking watchlist after adding movie...")
    response = requests.get(f"{BASE_URL}/watchlist/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', 0)
        print(f"✅ Watchlist now has {count} movie(s)")
        
        if count > 0:
            movies = data.get('watchlist', [])
            movie = movies[0]
            print(f"   Movie: {movie.get('movie_title')}")
            print(f"   Status: {movie.get('watch_status')}")
    
    # Step 5: Check if movie is in watchlist
    print("\n🔍 Checking if movie is in watchlist...")
    response = requests.get(f"{BASE_URL}/watchlist/check/550/", headers=headers)
    print(f"Check movie status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        in_watchlist = data.get('in_watchlist', False)
        print(f"✅ Movie in watchlist: {in_watchlist}")
    
    # Step 6: Toggle watch status
    print("\n🔄 Toggling watch status (mark as watched)...")
    response = requests.put(f"{BASE_URL}/watchlist/550/toggle/", headers=headers)
    print(f"Toggle status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {data.get('message', 'Status toggled')}")
    
    # Step 7: Get watchlist stats
    print("\n📊 Getting watchlist statistics...")
    response = requests.get(f"{BASE_URL}/watchlist/stats/", headers=headers)
    print(f"Stats status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total movies: {data.get('total_movies', 0)}")
        print(f"   Want to watch: {data.get('want_to_watch', 0)}")
        print(f"   Watched: {data.get('watched', 0)}")
    
    print("\n🎉 Watchlist test completed!")

if __name__ == "__main__":
    test_watchlist_operations()
