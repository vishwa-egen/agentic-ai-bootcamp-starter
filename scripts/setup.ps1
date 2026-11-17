# One-time setup for Windows. Safe to run again.
#   powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

# 1. Find a supported Python (3.12 to 3.14). Python 3.12 is the tested default.
$check = "import sys; sys.exit(0 if (3, 12) <= sys.version_info[:2] <= (3, 14) else 1)"
$candidates = @(
    @("py", "-3.12"), @("py", "-3.13"), @("py", "-3.14"),
    @("python"), @("python3")
)
$python = $null
foreach ($candidate in $candidates) {
    $exe = $candidate[0]
    $prefix = @()
    if ($candidate.Count -gt 1) { $prefix = $candidate[1..($candidate.Count - 1)] }
    if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
    try {
        & $exe @prefix -c $check 2>$null
        if ($LASTEXITCODE -eq 0) { $python = $candidate; break }
    } catch { }
}
if (-not $python) {
    Write-Host "No supported Python found. Install Python 3.12 and run this script again."
    Write-Host "  winget install -e --id Python.Python.3.12"
    exit 1
}
$pythonExe = $python[0]
$pythonArgs = @()
if ($python.Count -gt 1) { $pythonArgs = $python[1..($python.Count - 1)] }
$version = & $pythonExe @pythonArgs --version
Write-Host "==> Using $version"

# 2. Create the virtual environment. Everything installs into .venv, not your system.
if (-not (Test-Path ".venv")) {
    Write-Host "==> Creating the virtual environment in .venv"
    & $pythonExe @pythonArgs -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Could not create the virtual environment." }
}
$venvPython = ".\.venv\Scripts\python.exe"

# 3. Install the pinned libraries.
Write-Host "==> Installing libraries (a few minutes on the first run)"
& $venvPython -m pip install --quiet --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed." }
& $venvPython -m pip install --quiet -e ".[dev]" -c constraints.txt
if ($LASTEXITCODE -ne 0) { throw "Library install failed. See the messages above." }

# 4. Create your private settings file.
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "==> Created .env from .env.example"
}

# 5. Install the commit checks.
if (Test-Path ".git") {
    & ".\.venv\Scripts\pre-commit.exe" install | Out-Null
    Write-Host "==> Installed the pre-commit checks"
}

Write-Host ""
Write-Host "Setup complete. Next steps:"
Write-Host ""
Write-Host "  1. Open .env and replace every REPLACE_ME value."
Write-Host "  2. Activate the environment:   .\.venv\Scripts\Activate.ps1"
Write-Host "  3. Check your connections:     python -m bootcamp doctor"
Write-Host "  4. Open the app:               python -m bootcamp app"
