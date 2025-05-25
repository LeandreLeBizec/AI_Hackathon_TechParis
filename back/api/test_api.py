#!/usr/bin/env python3
"""
Test script for CV Analysis API

This script demonstrates how to test all the API endpoints.
Make sure the API server is running before executing this script.
"""

import requests
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_companies():
    """Test getting available companies"""
    print("🏢 Testing get companies...")
    response = requests.get(f"{BASE_URL}/companies")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    return response.json().get("companies", [])

def test_analyze_cv(pdf_path: str, company_name: str):
    """Test CV analysis endpoint"""
    print(f"📄 Testing CV analysis for company: {company_name}")
    
    # Check if PDF file exists
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    # Prepare the request
    with open(pdf_path, 'rb') as pdf_file:
        files = {'file': ('cv.pdf', pdf_file, 'application/pdf')}
        data = {'company_name': company_name}
        
        response = requests.post(f"{BASE_URL}/analyze-cv", files=files, data=data)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Analysis successful!")
        print(f"Processing time: {result['processing_time_seconds']} seconds")
        print(f"Fit score: {result['screening_test']['fit_score']}/5")
        print(f"Recommendation: {result['screening_test']['recommendation']}")
        print(f"Company description: {result['company_description']['description'][:100]}...")
        print(f"Number of interview questions: {len(result['company_values_questions']['questions'])}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_root_endpoint():
    """Test the root endpoint"""
    print("🏠 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting API tests...\n")
    
    # Test basic endpoints
    test_health_check()
    test_root_endpoint()
    
    # Get available companies
    companies = test_get_companies()
    
    if not companies:
        print("❌ No companies available for testing")
        return
    
    # Test CV analysis with the first available company
    company_name = companies[0]
    
    # You can specify your own PDF path here
    pdf_path = "data/candidates/CV_TTAYLOR_2025.pdf"  # Update this path
    
    test_analyze_cv(pdf_path, company_name)
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    main() 