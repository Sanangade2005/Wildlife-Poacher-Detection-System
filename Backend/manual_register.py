import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def register_user():
    payload = {
        "ranger_id": "manual_test_001",
        "first_name": "Manual",
        "last_name": "Test",
        "email_or_phone": "manual@test.com",
        "password": "password123",
        "repeat_password": "password123" # Just in case frontend sends this
    }
    
    print(f"Attempting to register: {payload}")
    try:
        resp = requests.post(f"{BASE_URL}/register", json=payload)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Request Failed: {e}")

if __name__ == "__main__":
    register_user()
