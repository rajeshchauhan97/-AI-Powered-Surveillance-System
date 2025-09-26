# setup_heroku.py
import os
import subprocess
import sys

def setup_heroku():
    print("🚀 Setting up Heroku deployment...")
    
    # Check if Heroku CLI is installed
    try:
        subprocess.run(["heroku", "--version"], check=True, capture_output=True)
        print("✅ Heroku CLI is installed")
    except:
        print("❌ Heroku CLI not found. Please install it from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Login to Heroku (if not already logged in)
    try:
        subprocess.run(["heroku", "login"], check=True)
    except:
        print("⚠️  Please login to Heroku manually when prompted")
    
    # Create Heroku app
    app_name = "movie-booking-system-algo"
    try:
        subprocess.run(["heroku", "create", app_name], check=True)
        print(f"✅ Heroku app created: {app_name}")
    except Exception as e:
        print(f"❌ Error creating Heroku app: {e}")
        # Try with random name
        subprocess.run(["heroku", "create"], check=True)
        print("✅ Heroku app created with random name")
    
    # Add PostgreSQL addon
    try:
        subprocess.run(["heroku", "addons:create", "heroku-postgresql:hobby-dev"], check=True)
        print("✅ PostgreSQL addon added")
    except Exception as e:
        print(f"⚠️  Could not add PostgreSQL: {e}")
        print("ℹ️  Using SQLite for demo (not recommended for production)")
    
    print("\n🎉 Heroku setup complete!")
    print("Next steps:")
    print("1. Run: git push heroku main")
    print("2. Run: heroku open")
    return True

if __name__ == "__main__":
    setup_heroku()