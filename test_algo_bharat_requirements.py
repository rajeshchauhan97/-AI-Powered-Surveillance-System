# test_algo_bharat_simple.py
import requests

BASE_URL = "https://movie-booking-system-15.onrender.com"

def test_basic_functionality():
    print("🎬 Testing Basic Algo Bharat Requirements\n")
    
    # Test 1: Check if API is accessible
    print("1. Testing API Accessibility")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return
    
    # Test 2: Check Health Endpoint
    print("\n2. Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Health Check: {response.json()}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 3: Check API Documentation
    print("\n3. Testing API Documentation")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ API Documentation is accessible")
        else:
            print("   ❌ API Docs not available")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 4: Check Movies Endpoint
    print("\n4. Testing Movies Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/movies/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            movies = response.json()
            print(f"   ✅ Movies API working: {len(movies)} movies found")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 5: Check Theaters Endpoint
    print("\n5. Testing Theaters Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/theaters/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            theaters = response.json()
            print(f"   ✅ Theaters API working: {len(theaters)} theaters found")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n" + "="*50)
    print("📋 DEPLOYMENT STATUS SUMMARY:")
    print("="*50)
    
    # Final verification
    print(f"\n🔗 Your Live API: {BASE_URL}")
    print(f"📚 API Documentation: {BASE_URL}/docs")
    print(f"❤️  Health Check: {BASE_URL}/health")
    
    print("\n✅ If all above tests pass, your Algo Bharat assignment meets requirements!")
    print("🎯 You can demonstrate all features through the API documentation.")

if __name__ == "__main__":
    test_basic_functionality()