@echo off
echo 🚀 Fixing railway.json JSON Error
echo ================================

echo 🗑️ Step 1: Removing problematic railway.json...
del railway.json 2>nul

echo 📝 Step 2: Creating clean railway.json...

:: Method 1: Simple one-line JSON
echo {"$schema": "https://railway.app/railway.schema.json","build": {"builder": "nixpacks","buildCommand": "pip install -r requirements.txt"},"deploy": {"startCommand": "uvicorn app.main:app --host=0.0.0.0 --port=$PORT","restartPolicyType": "ON_FAILURE"}} > railway.json

echo ✅ Step 3: Verifying the file was created...
if exist railway.json (
    echo ✅ railway.json created successfully
) else (
    echo ❌ Failed to create railway.json
    goto :error
)

echo 📄 Step 4: Displaying file content...
type railway.json

echo 🔄 Step 5: Pushing fix to GitHub...
git add railway.json
git commit -m "fix: Correct railway.json JSON syntax"
git push origin main

echo.
echo ✅ Fix completed!
echo 🚀 Now deploy on Railway: https://railway.app
goto :end

:error
echo ❌ Something went wrong. Please manually create railway.json.
pause
exit /b 1

:end
echo.
echo 🎉 railway.json is now fixed!
pause