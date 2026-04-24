#!/usr/bin/env python3
"""
Simple test script for the Internal Docs Q&A Agent backend
"""

import requests
import json
import time

def test_backend():
    """Test the backend endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Internal Docs Q&A Agent Backend")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Please start the Flask server first.")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Ask Question (Mock)
    print("\n2. Testing Question Answering...")
    try:
        test_question = "What is the company expense policy?"
        response = requests.post(
            f"{base_url}/ask",
            json={"question": test_question},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Question answering works")
            print(f"   Question: {test_question}")
            print(f"   Answer: {data.get('answer', 'No answer')}")
            print(f"   Sources: {data.get('sources', [])}")
        else:
            print(f"❌ Question answering failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Question answering error: {e}")
    
    # Test 3: Index Documents (Mock)
    print("\n3. Testing Document Indexing...")
    try:
        response = requests.post(f"{base_url}/index_docs", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Document indexing endpoint works")
            print(f"   Response: {data}")
        else:
            print(f"❌ Document indexing failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Document indexing error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Backend test completed!")
    return True

if __name__ == "__main__":
    test_backend() 