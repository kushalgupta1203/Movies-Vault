#!/usr/bin/env python3
"""
Test login and watchlist functionality
======================================
"""

import requests
import json


BASE_URL = "http://127.0.0.1:8000/api"

def test_login_and_watchlist():
    """Test login and then try to add to watchlist"""
    print("🔐 Testing login and watchlist...")
    
    # First, login with a user
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    try:
        # Login
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"  Login: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access')
            print(f"  Access token: {access_token[:20]}...")
            
            # Try to add movie to watchlist
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            watchlist_data = {
                "movie_id": "550"  # Fight Club
            }
            
            response = requests.post(f"{BASE_URL}/watchlist/add/", 
                                   json=watchlist_data, 
                                   headers=headers)
            print(f"  Add to watchlist: {response.status_code}")
            if response.status_code != 201:
                print(f"    Error: {response.text}")
            else:
                print(f"    Success: {response.json()}")
                
        else:
            print(f"    Login failed: {response.text}")
            
    except Exception as e:
        print(f"  ERROR: {e}")

def main():
    print("=" * 50)
    print("🧪 TESTING LOGIN AND WATCHLIST")
    print("=" * 50)
    print()
    
    test_login_and_watchlist()
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    main()
