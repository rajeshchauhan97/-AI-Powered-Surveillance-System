# simple_test.py
import requests

def simple_test():
    BASE_URL = "http://localhost:8000"
    
    print("🧪 Simple API Test")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Test movies list
    try:
        response = requests.get(f"{BASE_URL}/movies/")
        print(f"✅ Movies endpoint: {response.status_code}")
        print(f"Movies count: {len(response.json())}")
    except Exception as e:
        print(f"❌ Movies endpoint failed: {e}")

if __name__ == "__main__":
    simple_test()