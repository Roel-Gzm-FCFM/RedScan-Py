echo "Iniciando pipeline RedScan..."

mkdir -p examples

# Crear ID único de ejecución
RUN_ID=$(date +"%Y%m%d_%H%M%S")

# Función para escribir logs
log_event() {
  local module=$1
  local level=$2
  local event=$3
  local details=$4
  local timestamp=$(date +"%Y-%m-%dT%H:%M:%S")
  echo "{\"timestamp\": \"$timestamp\", \"run_id\": \"$RUN_ID\", \"module\": \"$module\", \"level\": \"$level\", \"event\": \"$event\", \"details\": \"$details\"}" >> examples/logs.jsonl
}

# Ejecutar el escaneo
echo "Ejecutando escaneo..."
python3 src/scanner.py > examples/scan_results.json
if [ $? -eq 0 ]; then
  log_event "scanner" "INFO" "Scan completed" "Resultados guardados en examples/scan_results.json"
else
  log_event "scanner" "ERROR" "Scan failed" "Error al ejecutar scanner.py"
  exit 1
fi

# Ejecutar el análisis con IA
echo "🧠 Analizando resultados con IA..."
python3 src/ai_summary.py examples/scan_results.json
if [ $? -eq 0 ]; then
  log_event "ai_summary" "INFO" "AI analysis done" "Archivo generado con resumen IA"
else
  log_event "ai_summary" "ERROR" "AI analysis failed" "Error al ejecutar ai_summary.py"
  exit 1
fi

# Log final
log_event "pipeline" "INFO" "Pipeline completed" "Ejecución completa sin errores"
echo "Pipeline completado."