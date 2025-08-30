@echo off
echo ==========================================
echo    TextMood DJ - API Key Setup
echo ==========================================
echo.
echo Please enter your API keys when prompted:
echo.

set /p youtube_key="Enter your YouTube Data API Key: "
set /p giphy_key="Enter your GIPHY API Key: "

echo.
echo Creating .env file...

(
echo # TextMood DJ API Keys
echo YOUTUBE_API_KEY=%youtube_key%
echo GIPHY_API_KEY=%giphy_key%
echo ALLOWED_ORIGIN=http://localhost:5173
echo.
echo # Database URL ^(optional, defaults to sqlite^)
echo # DB_URL=sqlite:///textmood.db
 ) > .env

echo.
echo ✅ API keys saved to .env file!
echo ✅ Your TextMood DJ is now ready to rock! 🎵
echo.
echo Next steps:
echo 1. Run: uvicorn app:app --reload --port 8000
echo 2. Open: test.html in your browser
echo 3. Test your mood detection!
echo.
pause
