# Bangla PDF OCR - Windows Dependency Installation Script
# This script checks for and installs necessary dependencies for Bangla PDF OCR on Windows.

# Check if the script is running with administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Write-Host "This script requires administrator privileges." -ForegroundColor Red
    Write-Host "Please run this script as an administrator." -ForegroundColor Yellow
    Write-Host "Right-click on the PowerShell icon and select 'Run as administrator'." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

function Find-Program {
    param (
        [string]$programName
    )
    $program = Get-Command $programName -ErrorAction SilentlyContinue
    if ($program) {
        return $program.Source
    }
    return $null
}

function Install-Poppler {
    $popplerUrl = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip"
    $popplerZip = "poppler.zip"
    $popplerDir = "C:\Program Files\poppler"

    Write-Host "Downloading Poppler..."
    Invoke-WebRequest -Uri $popplerUrl -OutFile $popplerZip

    Write-Host "Extracting Poppler..."
    Expand-Archive -Path $popplerZip -DestinationPath $popplerDir -Force
    Remove-Item $popplerZip

    # Find the correct Poppler bin directory
    $popplerBinPath = Get-ChildItem -Path $popplerDir -Recurse -Directory | Where-Object { $_.Name -eq "bin" } | Select-Object -First 1 -ExpandProperty FullName

    if (-not $popplerBinPath) {
        Write-Host "Error: Could not find Poppler bin directory"
        return $false
    }

    # Add Poppler to PATH
    $paths = [Environment]::GetEnvironmentVariable("Path", "Machine").Split(";")
    if ($paths -notcontains $popplerBinPath) {
        $paths += $popplerBinPath
        $newPath = $paths -join ";"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
    }

    Write-Host "Poppler installed successfully."
    return $true
}

function Install-Tesseract {
    $tesseractUrl = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe"
    $tesseractInstaller = "tesseract-installer.exe"

    Write-Host "Downloading Tesseract..."
    Invoke-WebRequest -Uri $tesseractUrl -OutFile $tesseractInstaller

    Write-Host "Installing Tesseract..."
    try {
        # Start the installer and wait for it to complete
        Start-Process -FilePath $tesseractInstaller -ArgumentList "/S" -Wait -NoNewWindow
    }
    catch {
        Write-Host "Error installing Tesseract: $_"
        return $false
    }
    finally {
        # Clean up the installer file
        Remove-Item $tesseractInstaller -ErrorAction SilentlyContinue
    }

    $tesseractPath = "C:\Program Files\Tesseract-OCR"

    # Add Tesseract to PATH
    $paths = [Environment]::GetEnvironmentVariable("Path", "Machine").Split(";")
    if ($paths -notcontains $tesseractPath) {
        $paths += $tesseractPath
        $newPath = $paths -join ";"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
    }

    Write-Host "Tesseract installed successfully."
    return $true
}

function Install-BengaliLanguageData {
    $tesseractPath = "C:\Program Files\Tesseract-OCR"
    $tessdataDir = Join-Path $tesseractPath "tessdata"
    $tessdataScriptDir = Join-Path $tessdataDir "script"
    if (-not (Test-Path $tessdataScriptDir)) {
        New-Item -ItemType Directory -Force -Path $tessdataScriptDir
    }
    $bengaliScriptUrl = "https://github.com/tesseract-ocr/tessdata/raw/main/script/Bengali.traineddata"
    $bengaliLangUrl = "https://github.com/tesseract-ocr/tessdata/raw/main/ben.traineddata"

    $success = $true

    if (-not (Test-Path (Join-Path $tessdataScriptDir "Bengali.traineddata"))) {
        Write-Host "Downloading Bengali script data..."
        try {
            Invoke-WebRequest -Uri $bengaliScriptUrl -OutFile (Join-Path $tessdataScriptDir "Bengali.traineddata")
        }
        catch {
            Write-Host "Error downloading Bengali script data: $_"
            $success = $false
        }
    }

    if (-not (Test-Path (Join-Path $tessdataDir "ben.traineddata"))) {
        Write-Host "Downloading Bengali language data..."
        try {
            Invoke-WebRequest -Uri $bengaliLangUrl -OutFile (Join-Path $tessdataDir "ben.traineddata")
        }
        catch {
            Write-Host "Error downloading Bengali language data: $_"
            $success = $false
        }
    }

    if ($success) {
        Write-Host "Bengali language data installed successfully."
    }
    return $success
}

# Check for Poppler
$pdftoppm = Find-Program "pdftoppm"
if (-not $pdftoppm) {
    Write-Host "Poppler not found. Installing..."
    $popplerInstalled = Install-Poppler
    if (-not $popplerInstalled) {
        Write-Host "Failed to install Poppler. Please install it manually."
    }
} else {
    Write-Host "Poppler found at: $pdftoppm"
}

# Check for Tesseract
$tesseract = Find-Program "tesseract"
if (-not $tesseract) {
    Write-Host "Tesseract not found. Installing..."
    $tesseractInstalled = Install-Tesseract
    if (-not $tesseractInstalled) {
        Write-Host "Failed to install Tesseract. Please install it manually."
    }
} else {
    Write-Host "Tesseract found at: $tesseract"
}

# Check for Bengali language files
$tesseractPath = "C:\Program Files\Tesseract-OCR"
$tessdataDir = Join-Path $tesseractPath "tessdata"
$bengaliScript = Join-Path $tessdataDir "script\Bengali.traineddata"
$bengaliLang = Join-Path $tessdataDir "ben.traineddata"

if (-not (Test-Path $bengaliScript) -or -not (Test-Path $bengaliLang)) {
    Write-Host "Bengali language files not found. Installing..."
    $bengaliInstalled = Install-BengaliLanguageData
    if (-not $bengaliInstalled) {
        Write-Host "Failed to install Bengali language files. Please install them manually."
    }
} else {
    Write-Host "Bengali language files found."
}

Write-Host "Windows dependencies setup completed."
Write-Host "Please restart your PowerShell or command prompt for the changes to take effect."