#!/usr/bin/env python3
"""
Simple test script for the dashboard functionality
"""

import json
import requests
from datetime import datetime

def test_dashboard_endpoints():
    """Test the dashboard endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Dashboard Endpoints")
    print("=" * 50)
    
    # Test 1: Get dashboard scores (should be empty initially)
    print("\n1. Testing GET /dashboard/scores (empty state)")
    try:
        response = requests.get(f"{base_url}/dashboard/scores")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📊 Total candidates: {data['total_candidates']}")
            print(f"🏢 Companies analyzed: {data['companies_analyzed']}")
            print(f"📈 Average fit score: {data['average_fit_score']}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Check if we can clear results
    print("\n2. Testing DELETE /dashboard/scores")
    try:
        response = requests.delete(f"{base_url}/dashboard/scores")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📝 Message: {data['message']}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Check available companies
    print("\n3. Testing GET /companies")
    try:
        response = requests.get(f"{base_url}/companies")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"🏢 Available companies: {data['companies']}")
            if data['companies']:
                print(f"💡 You can test CV analysis with company: {data['companies'][0]}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Dashboard endpoints are ready!")
    print("📋 To populate with data:")
    print("   1. Use POST /analyze-cv with a PDF file and company name")
    print("   2. Then check GET /dashboard/scores to see aggregated results")
    print("\n📖 API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    test_dashboard_endpoints() 