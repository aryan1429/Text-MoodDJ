#!/usr/bin/env python3

import requests

def test_health():
    url = "http://localhost:8000/api/session"
    
    try:
        response = requests.get(url)
        print(f"Health check - Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_health()
