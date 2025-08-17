#!/usr/bin/env python3

import requests
import io
import time

def test_voice_endpoint():
    url = "http://localhost:8002/api/analyze-voice"
    
    # Create a simple empty audio file for testing
    dummy_audio = b"dummy audio data"
    
    files = {
        'audio': ('test.webm', dummy_audio, 'audio/webm')
    }
    
    # First check if server is running
    try:
        health_response = requests.get("http://localhost:8002/api/health", timeout=5)
        print(f"Health check: {health_response.status_code}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    try:
        print("Sending voice analysis request...")
        response = requests.post(url, files=files, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Connection error - server may have crashed")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_voice_endpoint()
