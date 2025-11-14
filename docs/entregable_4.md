# Avance del Proyecto - Entregable 4

## 1. Flujo Técnico Consolidado

En este entregable, el proyecto ha sido reorganizado y consolidado en un flujo técnico funcional, cumpliendo con la estructura modular solicitada por el PIA.

* **Reorganización de `/src`:** El código fuente se ha movido a las carpetas de responsabilidad:
    * `src/acquisition/run_scan.py`
    * `src/reporting/ai_summary.py`
    * `src/utils/check_ssh.py`

* **Orquestación (PowerShell + Python):** El script `scripts/run_pipeline.ps1` actúa como el orquestador principal. Llama exitosamente a los módulos de Python en sus nuevas ubicaciones, demostrando el uso de dos lenguajes.

## 2. IA Integrada Funcionalmente

La Tarea 2 (Análisis con IA) está 100% integrada en el pipeline:

* **Manejo de API Key:** El script `run_pipeline.ps1` gestiona la clave de API de Google, pidiéndola al usuario y guardándola de forma segura en un `.gitignore` si es necesario.
* **Manejo de Errores (Retries):** El script `src/reporting/ai_summary.py` ha sido actualizado para incluir un bucle de reintentos (`retries`), lo que le da robustez contra fallos temporales de la API.
* **Salida en Markdown:** La salida de la IA ahora se guarda como `executive_summary.md` (en lugar de `.txt`), cumpliendo con el requisito de reporte final.

## 3. Evidencia y Logs

La ejecución del pipeline completo es reproducible y genera tres artefactos principales en la carpeta `/examples`:

1.  `scan_results.json`: La salida cruda de la Tarea 1 (Escaneo).
2.  `executive_summary_[fecha].md`: El reporte final en Markdown generado por la Tarea 2 (IA).
3.  `logs.jsonl`: Un log estructurado en formato JSON Lines que registra cada paso del orquestador `run_pipeline.ps1`.

## 4. Instrucciones de Ejecución

1.  Activar el entorno virtual: `.\.venv\Scripts\Activate.ps1`
2.  Navegar a la carpeta de scripts: `cd scripts`
3.  Ejecutar el pipeline: `powershell.exe -ExecutionPolicy Bypass -File .\run_pipeline.ps1`