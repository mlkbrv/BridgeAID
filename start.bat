@echo off
REM BridgeAID Docker Startup Script for Windows

echo 🚀 Starting BridgeAID Application...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.example .env
    echo ⚠️  Please edit .env file with your settings before running again.
    pause
    exit /b 1
)

REM Choose environment
echo Select environment:
echo 1) Development (with hot reload)
echo 2) Production (optimized)
set /p choice="Enter choice [1-2]: "

if "%choice%"=="1" (
    echo 🔧 Starting development environment...
    docker-compose -f docker-compose.dev.yml up --build
) else if "%choice%"=="2" (
    echo 🏭 Starting production environment...
    docker-compose -f docker-compose.prod.yml up -d --build
    echo ✅ Production environment started!
    echo 🌐 Application available at: http://localhost
    echo 📊 Admin panel: http://localhost/admin
    echo 🔗 API: http://localhost/api/
) else (
    echo ❌ Invalid choice. Exiting.
    pause
    exit /b 1
)

pause
