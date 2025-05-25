#!/usr/bin/env python3
"""
Startup script for CV Analysis API with SSL fix for Windows venv environments
"""

import os
import ssl
import sys
from pathlib import Path

def fix_conda_ssl_in_venv():
    """Fix conda SSL environment variables when using venv"""
    print("🔧 Fixing conda SSL variables for venv...")
    
    # These are the problematic conda paths you have
    problematic_ssl_vars = ['SSL_CERT_FILE', 'SSL_CERT_DIR']
    cleared = []
    
    for var in problematic_ssl_vars:
        value = os.environ.get(var)
        if value and ('conda' in value or 'miniconda' in value):
            print(f"❌ Clearing problematic conda SSL variable {var}: {value}")
            del os.environ[var]
            cleared.append(var)
    
    if cleared:
        print(f"✅ Cleared conda SSL variables: {', '.join(cleared)}")
    
    # Set up SSL for venv
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    
    print("✅ SSL configuration updated for venv")

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ['MISTRAL_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Create a .env file in the project root with:")
        print("   MISTRAL_API_KEY=your_actual_api_key_here")
        return False
    
    print("✅ Environment variables are set")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting CV Analysis API...")
    
    # Fix conda SSL issues for venv first
    fix_conda_ssl_in_venv()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Import and start the app
    try:
        print("📦 Loading FastAPI application...")
        # Import to verify it works, but don't pass the object to uvicorn
        from app import app
        import uvicorn
        
        print("🌐 Starting server on http://localhost:8000")
        print("📚 API documentation available at http://localhost:8000/docs")
        print("❤️  Health check at http://localhost:8000/health")
        print("\n🛑 Press Ctrl+C to stop the server\n")
        
        # Use import string instead of app object for reload to work properly
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the src/cv_reader directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 