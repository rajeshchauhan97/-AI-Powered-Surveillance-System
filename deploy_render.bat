@echo off
echo 🚀 Deploying to Render.com (Free Tier)
echo =====================================

echo 📦 Cleaning project files...
rmdir /S /Q app\__pycache__ 2>nul
rmdir /S /Q __pycache__ 2>nul
del /S *.pyc 2>nul
del railway.json 2>nul
del nixpacks.toml 2>nul

echo ⚙️ Creating Render configuration...
echo services: > render.yaml
echo   - type: web >> render.yaml
echo     name: movie-booking-system >> render.yaml
echo     env: python >> render.yaml
echo     plan: free >> render.yaml
echo     branch: main >> render.yaml
echo     buildCommand: pip install -r requirements.txt >> render.yaml
echo     startCommand: uvicorn app.main:app --host=0.0.0.0 --port=$PORT >> render.yaml

echo 📝 Updating requirements.txt...
echo fastapi==0.104.1 > requirements.txt
echo uvicorn==0.24.0 >> requirements.txt
echo sqlalchemy==2.0.23 >> requirements.txt
echo pydantic==2.5.0 >> requirements.txt
echo python-multipart==0.0.6 >> requirements.txt

echo 📤 Pushing to GitHub...
git add .
git commit -m "deploy: Ready for Render.com free tier"
git push origin main

echo.
echo ✅ Code pushed to GitHub!
echo.
echo 🌟 NEXT STEPS:
echo 1. Go to: https://render.com
echo 2. Sign up with GitHub
echo 3. Click 'New +' -> 'Web Service'
echo 4. Connect your repository
echo 5. Configure settings (free plan)
echo 6. Deploy!
echo.
echo 🎉 Render.com offers 750 FREE hours/month!

pause