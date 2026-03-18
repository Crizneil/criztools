# GH-CRIZ OMNI TOOL Installer
# Professional Deployment Script for PISCES Workstation

Write-Host "--- GH-CRIZ OMNI TOOL INSTALLER ---" -ForegroundColor Green

# Check for Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[-] Python not found. Please install Python 3.10+." -ForegroundColor Red
    exit 1
}

Write-Host "[+] Python detected." -ForegroundColor Cyan

# Install requirements
Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
python -m pip install PyGithub rich psutil python-dotenv --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "[-] Failed to install requirements." -ForegroundColor Red
    exit 1
}

Write-Host "[+] Dependencies installed." -ForegroundColor Cyan

# Check for main.py, download if missing
if (!(Test-Path main.py)) {
    Write-Host "[*] Downloading main.py from GitHub..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Crizneil/gh-criz-omni-tool/main/main.py" -OutFile "main.py"
}

Write-Host "[*] Launching GH-CRIZ OMNI TOOL..." -ForegroundColor Green
python main.py
