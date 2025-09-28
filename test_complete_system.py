# test_complete_system.py
import requests
import time

BASE_URL = "http://localhost:8000/api"

def test_complete_system():
    print("🎬 Testing Complete Movie Booking System\n")
    
    time.sleep(2)
    
    # Test health
    print("1. ✅ Testing Health Endpoint")
    response = requests.get("http://localhost:8000/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test creating a movie
    print("\n2. 🎥 Creating a Movie")
    movie_data = {
        "title": "The Matrix",
        "description": "Sci-fi action movie",
        "duration_minutes": 136,
        "genre": "Sci-Fi",
        "language": "English"
    }
    response = requests.post(f"{BASE_URL}/movies", json=movie_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        movie = response.json()
        print(f"   ✅ Created: {movie['title']} (ID: {movie['id']})")
    else:
        print(f"   ❌ Failed: {response.text}")
        return
    
    # Test creating a theater
    print("\n3. 🎭 Creating a Theater")
    theater_data = {
        "name": "Cineplex Downtown",
        "address": "123 Main St",
        "city": "Metropolis"
    }
    response = requests.post(f"{BASE_URL}/theaters", json=theater_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        theater = response.json()
        print(f"   ✅ Created: {theater['name']} (ID: {theater['id']})")
    else:
        print(f"   ❌ Failed: {response.text}")
        return
    
    # Test booking
    print("\n4. 🎫 Creating a Booking")
    booking_data = {
        "movie_id": 1,
        "theater_id": 1,
        "seats": 2
    }
    response = requests.post(f"{BASE_URL}/bookings", json=booking_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        booking = response.json()
        print(f"   ✅ Booking Successful!")
        print(f"   Booking ID: {booking['booking_id']}")
        print(f"   Movie: {booking['movie_title']}")
        print(f"   Theater: {booking['theater_name']}")
        print(f"   Seats: {booking['seats']}")
        print(f"   Total: ${booking['total_amount']}")
    else:
        print(f"   ❌ Failed: {response.text}")
        return
    
    print("\n🎉 ALL TESTS PASSED! Movie Booking System is working!")

if __name__ == "__main__":
    test_complete_system()