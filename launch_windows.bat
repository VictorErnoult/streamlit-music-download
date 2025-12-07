@echo off
REM Ginette la Cassette - Windows Launcher
REM Double-click this file to run the app

setlocal EnableDelayedExpansion

REM Change to script directory
cd /d "%~dp0"

echo ============================================
echo   📼 Ginette la Cassette 🎅
echo ============================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Python n'est pas installe.
    echo.
    echo Installation de Python...
    echo.
    echo Telechargement de Python depuis python.org...
    
    REM Download Python installer
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'python_installer.exe'}"
    
    if exist python_installer.exe (
        echo Installation de Python en cours...
        echo IMPORTANT: Coche "Add Python to PATH" pendant l'installation !
        echo.
        start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
        del python_installer.exe
        
        REM Refresh environment variables
        call :RefreshEnv
        
        REM Check again
        python --version >nul 2>&1
        if !errorlevel! neq 0 (
            echo.
            echo ❌ Python n'a pas pu etre installe automatiquement.
            echo.
            echo Installe Python manuellement depuis https://www.python.org/downloads/
            echo IMPORTANT: Coche "Add Python to PATH" pendant l'installation
            echo.
            pause
            exit /b 1
        )
        echo ✅ Python installe avec succes
        echo.
    ) else (
        echo ❌ Echec du telechargement de Python.
        echo.
        echo Installe Python manuellement depuis https://www.python.org/downloads/
        echo IMPORTANT: Coche "Add Python to PATH" pendant l'installation
        echo.
        pause
        exit /b 1
    )
)

REM Check for pip
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  pip n'est pas disponible.
    echo Installation de pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ❌ Echec de l'installation de pip.
        echo.
        pause
        exit /b 1
    )
    echo ✅ pip installe avec succes
    echo.
)

REM Check for ffmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  ffmpeg n'est pas installe.
    echo.
    echo Installation de ffmpeg...
    echo.
    
    REM Check for Chocolatey
    choco --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo Installation de Chocolatey (gestionnaire de paquets Windows)...
        echo.
        powershell -NoProfile -ExecutionPolicy Bypass -Command "& {[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))}"
        
        REM Refresh environment
        call :RefreshEnv
        
        choco --version >nul 2>&1
        if !errorlevel! neq 0 (
            echo.
            echo ❌ Echec de l'installation de Chocolatey.
            echo.
            echo SOLUTION MANUELLE:
            echo 1. Telecharge ffmpeg depuis https://www.gyan.dev/ffmpeg/builds/
            echo 2. Extrais le fichier ZIP
            echo 3. Ajoute le dossier bin au PATH Windows
            echo.
            pause
            exit /b 1
        )
        echo ✅ Chocolatey installe avec succes
        echo.
    )
    
    echo Installation de ffmpeg via Chocolatey...
    choco install ffmpeg -y
    
    REM Refresh environment
    call :RefreshEnv
    
    ffmpeg -version >nul 2>&1
    if !errorlevel! neq 0 (
        echo.
        echo ❌ Echec de l'installation de ffmpeg.
        echo.
        echo SOLUTION MANUELLE:
        echo 1. Telecharge ffmpeg depuis https://www.gyan.dev/ffmpeg/builds/
        echo 2. Extrais le fichier ZIP
        echo 3. Ajoute le dossier bin au PATH Windows
        echo.
        pause
        exit /b 1
    )
    echo ✅ ffmpeg installe avec succes
    echo.
)

REM Install/Update Python dependencies
echo 📦 Verification des dependances Python...
python -m pip install -r requirements.txt --quiet --upgrade
if %errorlevel% neq 0 (
    echo ❌ Echec de l'installation des dependances Python.
    echo.
    pause
    exit /b 1
)
echo ✅ Dependances Python a jour
echo.

echo ============================================
echo   ✅ Tout est pret !
echo ============================================
echo.
echo 🚀 Lancement de l'application...
echo.
echo L'application va s'ouvrir dans ton navigateur.
echo Pour arreter l'application, ferme cette fenetre.
echo.

REM Launch Streamlit
python -m streamlit run app.py --server.headless false --browser.gatherUsageStats false

REM If there's an error, keep window open
if %errorlevel% neq 0 (
    echo.
    echo ❌ L'application a rencontre une erreur.
    echo.
    pause
)

exit /b 0

REM Function to refresh environment variables
:RefreshEnv
REM Refresh PATH from registry
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SysPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "UserPath=%%b"
set "PATH=%SysPath%;%UserPath%"
exit /b 0

