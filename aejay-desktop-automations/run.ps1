# Navigate to script directory
Set-Location -Path $PSScriptRoot

# Activate venv and run Python script
& ./venv/Scripts/Activate.ps1
python ./main.py

