@echo off
echo ==========================================
echo   Forest Guard AI - Startup Script
echo ==========================================

echo.
echo [1/3] Starting Backend Server...
start "Backend Server" cmd /k "cd Backend && python app.py"

echo.
echo [2/3] Starting Frontend Server...
start "Frontend Server" cmd /k "cd forest-guard-ai && npm run dev"

echo.
echo [3/3] Opening Application in Browser...
echo Waiting for servers to initialize...
timeout /t 5 >nul
start http://localhost:5173

echo.
echo ==========================================
echo   Application Started!
echo   Backend: http://localhost:5000
echo   Frontend: http://localhost:5173
echo ==========================================
pause
