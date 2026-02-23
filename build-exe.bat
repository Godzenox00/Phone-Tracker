@echo off
REM ============================================
REM GhostTrack v3.0 - Build EXE Script
REM ============================================
REM This script builds the GhostTrack Electron app
REM into a portable Windows .exe file.
REM
REM Prerequisites:
REM   - Node.js 18+ (https://nodejs.org)
REM   - npm (comes with Node.js)
REM ============================================

title GhostTrack Build Tool
color 0A

echo.
echo  ============================================
echo   GhostTrack v3.0 - Build Tool
echo  ============================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Node.js is not installed!
    echo  Please install Node.js from https://nodejs.org
    echo.
    pause
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] npm is not installed!
    echo  Please install Node.js from https://nodejs.org
    echo.
    pause
    exit /b 1
)

REM Display versions
echo  [INFO] Node.js version:
node --version
echo  [INFO] npm version:
npm --version
echo.

REM Navigate to electron-app directory
cd /d "%~dp0electron-app"

if not exist "package.json" (
    echo  [ERROR] package.json not found in electron-app directory!
    echo  Make sure you're running this from the GhostTrack root folder.
    pause
    exit /b 1
)

REM Install dependencies
echo  [1/3] Installing dependencies...
echo.
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo  [2/3] Dependencies installed successfully.
echo.

REM Build the exe
echo  [3/3] Building portable EXE...
echo  This may take a few minutes on first build.
echo.
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  [ERROR] Build failed!
    echo  Check the error messages above.
    pause
    exit /b 1
)

echo.
echo  ============================================
echo   BUILD COMPLETE!
echo  ============================================
echo.
echo  Your portable EXE is located in:
echo    %~dp0dist\
echo.
echo  Look for: GhostTrack-*-Portable.exe
echo.

REM Open the dist folder
if exist "%~dp0dist" (
    explorer "%~dp0dist"
)

pause
