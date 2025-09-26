# test_complete_system.py
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_complete_system():
    print("🎬 Testing Complete Movie Booking System\n")
    
    # 1. Test Health
    print("1. ✅ Testing Health Endpoint")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}, Database: {response.json().get('database')}")
    
    # 2. Create a Movie
    print("\n2. 🎥 Creating a Movie")
    movie_data = {
        "title": "Avatar: The Way of Water",
        "description": "Jake Sully lives with his newfound family formed on the planet of Pandora.",
        "duration_minutes": 192,
        "genre": "Sci-Fi, Adventure",
        "language": "English",
        "release_date": "2022-12-16T00:00:00"
    }
    response = requests.post(f"{BASE_URL}/movies/", json=movie_data)
    movie = response.json()
    print(f"   Created: {movie['title']} (ID: {movie['id']})")
    
    # 3. Create a Theater
    print("\n3. 🏪 Creating a Theater")
    theater_data = {
        "name": "Megaplex Cinemas",
        "address": "789 Entertainment District",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62701"
    }
    response = requests.post(f"{BASE_URL}/theaters/", json=theater_data)
    theater = response.json()
    print(f"   Created: {theater['name']} (ID: {theater['id']})")
    
    # 4. Create a Theater Hall with seating layout
    print("\n4. 💺 Creating Theater Hall with Seating Layout")
    hall_data = {
        "theater_id": theater['id'],
        "name": "IMAX Screen 1",
        "layout": [
            {"row_number": 1, "total_seats": 7},
            {"row_number": 2, "total_seats": 8},
            {"row_number": 3, "total_seats": 8},
            {"row_number": 4, "total_seats": 8},
            {"row_number": 5, "total_seats": 7},
            {"row_number": 6, "total_seats": 6}
        ]
    }
    response = requests.post(f"{BASE_URL}/theaters/halls", json=hall_data)
    hall = response.json()
    print(f"   Created: {hall['name']} with {hall['total_seats']} seats")
    
    # 5. Create a Show
    print("\n5. 🕐 Creating a Movie Show")
    show_time = datetime.now() + timedelta(hours=2)
    end_time = show_time + timedelta(minutes=movie['duration_minutes'])
    
    show_data = {
        "movie_id": movie['id'],
        "hall_id": hall['id'],
        "start_time": show_time.isoformat(),
        "end_time": end_time.isoformat(),
        "price": 15.50
    }
    response = requests.post(f"{BASE_URL}/shows/", json=show_data)
    show = response.json()
    print(f"   Created Show: {movie['title']} at {show_time.strftime('%H:%M')} (ID: {show['id']})")
    
    # 6. Test Booking System
    print("\n6. 🎟️ Testing Booking System")
    booking_data = {
        "show_id": show['id'],
        "seat_selections": [
            {"row_number": 1, "seat_number": 1},
            {"row_number": 1, "seat_number": 2},
            {"row_number": 1, "seat_number": 3}
        ]
    }
    
    # Try individual booking
    response = requests.post(f"{BASE_URL}/bookings/book", json=booking_data)
    if response.status_code == 200:
        booking = response.json()
        print(f"   ✅ Booking Successful!")
        print(f"   Booking Reference: {booking['booking_reference']}")
        print(f"   Total Amount: ${booking['total_amount']}")
        print(f"   Seats Booked: {len(booking['booked_seats'])}")
    else:
        print(f"   ❌ Booking Failed: {response.text}")
    
    # 7. Test Group Booking with Suggestions
    print("\n7. 👥 Testing Group Booking with Suggestions")
    group_booking_data = {
        "show_id": show['id'],
        "seat_selections": [
            {"row_number": 2, "seat_number": 1},
            {"row_number": 2, "seat_number": 2},
            {"row_number": 2, "seat_number": 3},
            {"row_number": 2, "seat_number": 4}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/bookings/book-together", json=group_booking_data)
    if response.status_code == 200:
        result = response.json()
        if result['original_show_unavailable']:
            print("   ⚠️ Original show seats not available together")
            print(f"   Found {len(result['suggestions'])} alternative suggestions")
        else:
            print("   ✅ Group booking successful!")
    
    # 8. Test Analytics
    print("\n8. 📊 Testing Analytics")
    response = requests.get(f"{BASE_URL}/analytics/movie/{movie['id']}/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"   Movie Analytics for: {stats['movie_title']}")
        print(f"   Total Bookings: {stats['stats']['total_bookings']}")
        print(f"   Total Revenue: ${stats['stats']['total_revenue']:.2f}")
    
    # 9. List All Data
    print("\n9. 📋 Summary of Created Data")
    
    response = requests.get(f"{BASE_URL}/movies/")
    movies_list = response.json()
    print(f"   Movies: {len(movies_list)}")
    
    response = requests.get(f"{BASE_URL}/theaters/")
    theaters_list = response.json()
    print(f"   Theaters: {len(theaters_list)}")
    
    response = requests.get(f"{BASE_URL}/shows/")
    shows_list = response.json()
    print(f"   Shows: {len(shows_list)}")
    
    print(f"\n🎉 Complete System Test Finished Successfully!")
    print(f"🔗 API Documentation: {BASE_URL}/docs")

if __name__ == "__main__":
    test_complete_system()