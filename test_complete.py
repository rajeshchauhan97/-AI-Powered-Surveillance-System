import requests
import time
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server():
    """Wait for server to start"""
    print("⏳ Waiting for server to start...")
    for i in range(10):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running!")
                return True
        except:
            print(f"   Attempt {i+1}/10 - Server not ready yet...")
            time.sleep(2)
    return False

def test_complete_system():
    print("🎬 TESTING COMPLETE MOVIE BOOKING SYSTEM")
    print("=" * 50)
    
    # Wait for server to start
    if not wait_for_server():
        print("❌ Server failed to start. Please run: uvicorn main:app --reload")
        return
    
    # 1. Health Check
    print("1. 🔍 Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code} - {response.json()}")
    
    # 2. Create Movie
    print("\n2. 🎥 Create Movie")
    movie_data = {
        "title": "The Dark Knight",
        "duration": 152,
        "genre": "Action",
        "rating": 9.0
    }
    response = requests.post(f"{BASE_URL}/movies", json=movie_data)
   