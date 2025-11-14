# --- CONFIGURACIÓN AVANZADA DE CODIFICACIÓN ---
# 1. Asegura que la consola MUESTRE caracteres UTF-8 (acentos, ¿)
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
# 2. Asegura que los COMANDOS (Write-Host, Out-File) ESCRIBAN en UTF-8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

Write-Host "Iniciando pipeline RedScan..."

# Mover a la carpeta raíz del proyecto (una carpeta arriba de /scripts)
Set-Location "$PSScriptRoot\.."

# Definir la ruta del archivo de la API Key
$apiKeyFile = "google_api_key.txt"

# Crear carpeta de salida si no existe
if (-not (Test-Path "examples")) {
    New-Item -ItemType Directory -Path "examples" | Out-Null
}

# Crear ID único de ejecución
$RUN_ID = Get-Date -Format "yyyyMMdd_HHmmss"

# --- Función de Registro (Logging) ---
function Log-Event {
    param(
        [string]$Module,
        [string]$Level,
        [string]$Event,
        [string]$Details
    )
    $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
    $entry = @{
        timestamp = $timestamp
        run_id    = $RUN_ID
        module    = $Module
        level     = $Level
        event     = $Event
        details   = $Details
    } | ConvertTo-Json -Depth 5
    Add-Content -Path "examples/logs.jsonl" -Value $entry
}

# 1) Ejecutar escaneo (genera examples/scan_results.json)
Write-Host "Ejecutando escaneo..."
.\.venv\Scripts\python.exe "src/run_scan.py"
if ($LASTEXITCODE -eq 0) {
    Log-Event -Module "scanner" -Level "INFO" -Event "Scan completed" -Details "Resultados guardados en examples/scan_results.json"
} else {
    Write-Host "[ERROR] El script de escaneo (run_scan.py) falló." -ForegroundColor Red
    Log-Event -Module "scanner" -Level "ERROR" -Event "Scan failed" -Details "Error al ejecutar run_scan.py"
    exit 1
}

# ----------------------------------------------------
# 2) Buscar, Pedir y Guardar API Key
# ----------------------------------------------------
$ApiKey = ""
if (Test-Path $apiKeyFile) {
    $ApiKey = Get-Content $apiKeyFile
    $env:GOOGLE_API_KEY = $ApiKey
    Log-Event -Module "pipeline" -Level "INFO" -Event "API Key found" -Details "Clave API cargada desde archivo local."
} else {
    # (¡Acentos restaurados!)
    Write-Host "No se encontró un archivo de API key." -ForegroundColor Yellow
    $ApiKey = Read-Host "Por favor, ingresa tu clave de API de Google Gemini"
    $env:GOOGLE_API_KEY = $ApiKey
    
    # (¡'¿' restaurado!)
    $guardar = Read-Host "¿Deseas guardar esta clave para futuras ejecuciones? (S/N)"
    if ($guardar -match "^[Ss]$") {
        $ApiKey | Out-File $apiKeyFile
        Write-Host "Clave API guardada en $apiKeyFile" -ForegroundColor Green
        Log-Event -Module "pipeline" -Level "INFO" -Event "API Key provided" -Details "Clave API ingresada por el usuario y guardada en archivo."
    } else {
        Log-Event -Module "pipeline" -Level "INFO" -Event "API Key provided" -Details "Clave API ingresada por el usuario (solo para esta sesión)."
    }
}

# 3) Ejecutar análisis con IA
Write-Host "Analizando resultados con IA..."

# Capturamos TODA la salida de Python (stdout y stderr) en una variable
# '2>&1' significa "redirige el canal de error (2) al canal de salida (1)"
$pythonOutput = .\.venv\Scripts\python.exe "src/ai_summary.py" "examples/scan_results.json" 2>&1

# Verificamos si el comando de Python falló
if ($LASTEXITCODE -eq 0) {
    # Éxito
    Write-Host "[IA] Análisis completado. Revisa la carpeta /examples/." -ForegroundColor Green
    Log-Event -Module "ai_summary" -Level "INFO" -Event "AI analysis done" -Details "Resumen generado"
} else {
    # Fracaso. Mostramos NUESTRO error en español.
    Write-Host "------------------------------------------------------------" -ForegroundColor Red
    Write-Host "[IA] ERROR: El script de análisis de IA ('ai_summary.py') falló." -ForegroundColor Red
    Write-Host "[IA] CAUSA PROBABLE: La clave API de Google ('$ApiKey') no es válida." -ForegroundColor Red
    Write-Host "Por favor, borra el archivo 'google_api_key.txt' (si existe) y" -ForegroundColor Red
    Write-Host "vuelve a ejecutar el script con una clave API correcta." -ForegroundColor Red
    Write-Host "---"
    Write-Host "[DEBUG] Mensaje original de Python (en inglés):" -ForegroundColor Gray
    Write-Host "$pythonOutput" -ForegroundColor Gray # Imprime el error real en inglés
    Write-Host "------------------------------------------------------------" -ForegroundColor Red
    Log-Event -Module "ai_summary" -Level "ERROR" -Event "AI analysis failed" -Details "Error al ejecutar ai_summary.py - API Key invalida."
    exit 1
}

# 4) Log final
Log-Event -Module "pipeline" -Level "INFO" -Event "Pipeline completed" -Details "Ejecución completa sin errores"
Write-Host "Pipeline completado."