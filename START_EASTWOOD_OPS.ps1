# EastWood Ops / The Buch - Native Launcher
$ErrorActionPreference = "SilentlyContinue"
$BuchRoot = "Z:\36_chambers\The_Buch"
$BackendDir = Join-Path $BuchRoot "backend\app"
$PythonExe = Join-Path $BuchRoot "backend\venv\Scripts\python.exe"
$Port = 4149
$Url = "http://localhost:$Port"

# Sprawdzenie czy python.exe istnieje
if (-not (Test-Path $PythonExe)) {
    [System.Windows.Forms.MessageBox]::Show("Nie znaleziono środowiska Python: $PythonExe", "EastWood Ops Error", 0, 16)
    exit 1
}

# Sprawdzenie czy serwer na porcie 4149 już nasłuchuje
$activeConn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if (-not $activeConn) {
    $env:PORT = "$Port"
    Start-Process -FilePath $PythonExe -ArgumentList "main.py" -WorkingDirectory $BackendDir -WindowStyle Hidden
    
    # Oczekiwanie na gotowość serwera (max 10s)
    $maxAttempts = 20
    $ready = $false
    for ($i = 0; $i -lt $maxAttempts; $i++) {
        Start-Sleep -Milliseconds 500
        try {
            $resp = Invoke-RestMethod -Uri "$Url/api/health" -TimeoutSec 2 -ErrorAction Stop
            if ($resp.status -eq "ok") {
                $ready = $true
                break
            }
        } catch {
            # czekamy dalej
        }
    }
}

# Otwórz interfejs w przeglądarce
Start-Process $Url
