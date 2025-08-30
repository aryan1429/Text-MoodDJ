#!/usr/bin/env python3

import requests

def test_session_endpoint():
    url = "http://localhost:8001/api/session"
    
    try:
        print("Testing session endpoint...")
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_session_endpoint()
