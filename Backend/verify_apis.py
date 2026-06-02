import requests
import time
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_apis():
    ranger_id = "test_ranger_001"
    password = "password123"
    new_password = "newpassword456"

    print("--- Starting Verification ---")

    # 1. Register (or ensure user exists)
    print(f"\n1. Registering user {ranger_id}...")
    register_payload = {
        "ranger_id": ranger_id,
        "first_name": "Test",
        "last_name": "Ranger",
        "email_or_phone": "test@example.com",
        "password": password
    }
    
    # Try to register, if fails maybe user exists
    resp = requests.post(f"{BASE_URL}/register", json=register_payload)
    if resp.status_code == 201:
        print("User registered successfully.")
    elif resp.status_code == 400 and "already exists" in resp.json().get("message", ""):
        print("User already exists, proceeding.")
    else:
        print(f"Registration failed: {resp.status_code} - {resp.text}")
        # If we can't ensure user exists, we might fail later, but let's try login to check if password matches what we assume
        # Or just proceed.
    
    # 2. Get Profile
    print(f"\n2. Getting profile for {ranger_id}...")
    resp = requests.get(f"{BASE_URL}/officer-profile/{ranger_id}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Profile retrieved: {data}")
        assert data["ranger_id"] == ranger_id
        assert data["first_name"] == "Test" or data["first_name"] == "Updated"  # Allow if previous run changed it
    else:
        print(f"Failed to get profile: {resp.status_code} - {resp.text}")
        sys.exit(1)

    # 3. Update Profile
    print(f"\n3. Updating profile for {ranger_id}...")
    update_payload = {
        "first_name": "Updated",
        "last_name": "Name",
        "password": new_password
    }
    resp = requests.put(f"{BASE_URL}/officer-profile/{ranger_id}", json=update_payload)
    if resp.status_code == 200:
        print("Profile updated successfully.")
    else:
        print(f"Failed to update profile: {resp.status_code} - {resp.text}")
        sys.exit(1)

    # 4. Verify Update (Get Profile again)
    print(f"\n4. Verifying update for {ranger_id}...")
    resp = requests.get(f"{BASE_URL}/officer-profile/{ranger_id}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Profile retrieved: {data}")
        if data["first_name"] == "Updated" and data["last_name"] == "Name":
            print("Name update verified.")
        else:
            print("Name update FAILED.")
            sys.exit(1)
    else:
        print(f"Failed to get profile: {resp.status_code} - {resp.text}")
        sys.exit(1)

    # 5. Verify Password Change (Login)
    print(f"\n5. Verifying password change (Login)...")
    login_payload = {
        "email_or_phone": "test@example.com",
        "password": new_password
    }
    resp = requests.post(f"{BASE_URL}/login", json=login_payload)
    if resp.status_code == 200:
        print("Login with new password successful.")
    else:
        print(f"Login failed: {resp.status_code} - {resp.text}")
        sys.exit(1)
        
    print("\n--- Verification Passed ---")
    
    # Optional: cleanup
    # This part would need a delete API or direct DB access, skipping for now
    # as we want to inspect the state.

if __name__ == "__main__":
    try:
        # Simple check if server is up
        requests.get(BASE_URL)
    except requests.exceptions.ConnectionError:
        print("Server is not running. Please run app.py first.")
        sys.exit(1)
        
    test_apis()
