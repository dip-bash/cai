# Check for required tools
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed. Please install Git and run this script again."
    exit
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python and run this script again."
    exit
}
if (-not (Get-Command fish -ErrorAction SilentlyContinue)) {
    Write-Host "Fish shell is not installed. Please install Fish and run this script again."
    exit
}

# Define paths
$caiPath = "$env:USERPROFILE\cai"
$venvPath = "$caiPath\cai_venv"

# Clone the repository
if (Test-Path $caiPath) {
    Remove-Item -Recurse -Force $caiPath
}
git clone https://github.com/dip-bash/cai.git $caiPath

# Create virtual environment
python -m venv $venvPath

# Activate virtual environment
& "$venvPath\Scripts\Activate.ps1"

# Install uv
pip install uv

# Install dependencies
uv pip install -r "$caiPath\requirements.txt"

# Add alias to Fish config
$fishConfig = "$env:USERPROFILE\.config\fish\config.fish"
if (-not (Test-Path $fishConfig)) {
    New-Item -Path $fishConfig -ItemType File -Force
}
Add-Content -Path $fishConfig -Value "alias cai=`"$HOME/cai/cai_venv/Scripts/python.exe $HOME/cai/cai.py`""

# Print message
Write-Host -ForegroundColor Green "for help type cai -h/--help"
