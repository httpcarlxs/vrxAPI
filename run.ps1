param (
    [string]$dias
)

if (-not $dias) {
    Write-Host "Uso: .\run.ps1 --dias <N_DIAS>"
    exit 1
}

if (-not (Test-Path -Path "venv")) {
    Write-Host "Criando ambiente virtual..."
    python -m venv venv
}

& venv\Scripts\Activate
pip install -r requirements.txt
python app.py $dias
