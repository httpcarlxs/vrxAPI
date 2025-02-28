param (
    [string]$dias
)

if (-not $dias) {
    Write-Host "Uso: .\run.ps1 --dias <N_DIAS>"
    exit 1
}

& venv\Scripts\Activate
pip install -r requirements.txt
python app.py $dias
