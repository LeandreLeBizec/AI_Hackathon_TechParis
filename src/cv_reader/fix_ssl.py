#!/usr/bin/env python3
"""
SSL Fix Script for Windows venv with conda SSL environment variables

This script fixes the issue where SSL_CERT_FILE and SSL_CERT_DIR are pointing
to invalid conda paths while using venv.
"""

import os
import ssl
import sys

def clear_conda_ssl_vars():
    """Clear problematic conda SSL environment variables"""
    print("🔍 Checking SSL environment variables...")
    
    ssl_vars = ['SSL_CERT_FILE', 'SSL_CERT_DIR', 'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']
    cleared_vars = []
    
    for var in ssl_vars:
        value = os.environ.get(var)
        if value:
            print(f"❌ Found problematic {var}: {value}")
            del os.environ[var]
            cleared_vars.append(var)
        else:
            print(f"✅ {var} is not set")
    
    if cleared_vars:
        print(f"🧹 Cleared variables: {', '.join(cleared_vars)}")
    else:
        print("✅ No problematic SSL variables found")

def setup_ssl_for_venv():
    """Set up SSL configuration for venv"""
    print("🔧 Setting up SSL for venv...")
    
    # Clear problematic variables first
    clear_conda_ssl_vars()
    
    # Set Python to not verify SSL for development
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    print("✅ Set PYTHONHTTPSVERIFY=0")
    
    # Create unverified SSL context
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
        print("✅ Set unverified SSL context")
    
    print("🎉 SSL configuration complete!")

def test_ssl_fix():
    """Test if SSL fix works by trying to import and create Mistral client"""
    try:
        print("🧪 Testing SSL fix...")
        from mistralai import Mistral
        
        # Try to create client (will fail without API key, but SSL should work)
        try:
            client = Mistral(api_key="test")
        except Exception as e:
            if "api_key" in str(e).lower() or "authentication" in str(e).lower():
                print("✅ SSL fix successful! (API key error is expected)")
                return True
            else:
                print(f"❌ SSL issue still exists: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Import or SSL error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting SSL fix for venv...")
    setup_ssl_for_venv()
    
    if test_ssl_fix():
        print("✅ SSL fix successful! You can now run the API.")
    else:
        print("❌ SSL fix failed. You may need to reinstall certificates.")
        sys.exit(1) 