#!/usr/bin/env python3
"""
Quick test for MongoDB authentication fix
=========================================
"""

import requests
import json

# Base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_movies_without_auth():
    """Test that movies endpoints work without authentication"""
    print("🎬 Testing movies endpoints without authentication...")
    
    endpoints = [
        "/movies/popular/?page=1",
        "/movies/trending/?page=1", 
        "/movies/top-rated/?page=1"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"  {endpoint}: {response.status_code}")
            if response.status_code != 200:
                print(f"    Error: {response.text[:100]}...")
        except Exception as e:
            print(f"  {endpoint}: ERROR - {e}")

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("🔐 Testing authentication endpoints...")
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/auth/health/")
        print(f"  Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"    Response: {response.json()}")
    except Exception as e:
        print(f"  Health check: ERROR - {e}")
    
    # Test registration (without email)
    try:
        register_data = {
            "username": "testuser123",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        print(f"  Registration: {response.status_code}")
        if response.status_code != 201:
            print(f"    Error: {response.text[:100]}...")
        else:
            print(f"    Success: User created")
    except Exception as e:
        print(f"  Registration: ERROR - {e}")

def main():
    print("=" * 50)
    print("🧪 TESTING MONGODB AUTHENTICATION FIX")
    print("=" * 50)
    print()
    
    test_movies_without_auth()
    print()
    test_auth_endpoints()
    
    print()
    print("=" * 50)
    print("✅ Test completed! Check results above.")
    print("=" * 50)

if __name__ == "__main__":
    main()
