# Fichas Técnicas del Proyecto

A continuación, se detallan las tres tareas de ciberseguridad interrelacionadas que componen el núcleo de RedScan-Py.

---

## Ficha Técnica: Tarea 1 - Adquisición de Objetivos

* **Título de la tarea:** Tarea 1: Detección de IP Local y Carga de Vectores de Ataque
* **Propósito (2–3 frases):** Identificar la dirección IPv4 de la máquina local para establecerla como objetivo de auto-auditoría. Simultáneamente, cargar las listas de usuarios y contraseñas desde archivos externos (`users.txt`, `passwords.txt`) para preparar la fase de pruebas.
* **Entradas (formatos y ejemplos):**
    * `users.txt` (Archivo de texto plano, un usuario por línea).
    * `passwords.txt` (Archivo de texto plano, una contraseña por línea).
* **Salidas (formatos y ejemplos):**
    * **IP Local (String):** `"192.168.56.1"`.
    * **Listas (Python):** `["root", "admin"]`, `["123456", "password"]`.
* **Descripción del procedimiento (narración objetiva de las transformaciones):** El módulo `src/acquisition/run_scan.py` ejecuta el comando `ipconfig` del sistema operativo mediante `subprocess.check_output`. La salida de texto se parsea usando una expresión regular (`re.search`) para extraer la dirección IPv4. Paralelamente, la función `cargar_lista` lee los archivos `users.txt` y `passwords.txt` y los convierte en listas de Python.
* **Complejidad técnica (qué de las dimensiones listadas usa la tarea):**
    * Automatización básica (orquesta el comando `ipconfig`).
    * Procesamiento/parsing de salidas (extrae campos de texto plano con `re`).
    * Uso de una librería para manipular datos (`subprocess` y `re`).
* **Artefactos de evidencia entregados (rutas dentro del repo):**
    * `src/acquisition/run_scan.py`
    * `users.txt`
    * `passwords.txt`
* **Riesgos y controles éticos (cómo se mitigaron):** Tarea de bajo riesgo. Solo lee la configuración local (`ipconfig`) y archivos de texto.
* **Dependencias (comandos, librerías, variables de entorno):**
    * Librerías Python: `subprocess`, `re` (estándar).

---

## Ficha Técnica: Tarea 2 - Prueba de Credenciales SSH

* **Título de la tarea:** Tarea 2: Verificación de Credenciales SSH
* **Propósito (2–3 frases):** Probar sistemáticamente cada combinación de usuario y contraseña (obtenidas de la Tarea 1) contra el servicio SSH del host objetivo. El fin es identificar configuraciones inseguras y generar un reporte de hallazgos (éxitos y fallos).
* **Entradas (formatos y ejemplos):**
    * **IP (String):** `"192.168.56.1"`.
    * **Listas (Python):** `["root", "admin"]`, `["123456", "password"]`.
* **Salidas (formatos y ejemplos):**
    * **Formato:** Archivo JSON.
    * **Ejemplo:** `examples/scan_results.json`.
* **Descripción del procedimiento (narración objetiva de las transformaciones):** El script `src/acquisition/run_scan.py` itera sobre las listas de usuarios y contraseñas en bucles anidados. En cada iteración, invoca la función `check_ssh` del módulo `src/utils/check_ssh.py`. Esta función usa `paramiko` para intentar la conexión, manejando excepciones como `AuthenticationException` o `TimeoutError` y devolviendo `True` o `False`. Todos los resultados (éxitos y fallos) se agregan a una lista y se escriben en `scan_results.json`.
* **Complejidad técnica (qué de las dimensiones listadas usa la tarea):**
    * Uso de una librería especializada de ciberseguridad (`paramiko`).
    * Automatización básica (bucles anidados para fuerza bruta controlada).
* **Artefactos de evidencia entregados (rutas dentro del repo):**
    * `src/acquisition/run_scan.py`
    * `src/utils/check_ssh.py`
    * `examples/scan_results.json`
* **Riesgos y controles éticos (cómo se mitigaron):** Riesgo de bloqueo de cuenta. Se mitiga al estar enfocado en un entorno de auto-auditoría local. La Declaración Ética prohíbe su uso en sistemas de terceros.
* **Dependencias (comandos, librerías, variables de entorno):**
    * Librería Python: `paramiko`.

---

## Ficha Técnica: Tarea 3 - Análisis y Reporte Ejecutivo con IA

* **Título de la tarea:** Tarea 3: Análisis y Reporte Ejecutivo con IA
* **Propósito (2–3 frases):** Consumir el archivo JSON generado por la Tarea 2 y enviarlo a un modelo de IA (Google Gemini) para generar un resumen ejecutivo en lenguaje natural y formato Markdown.
* **Entradas (formatos y ejemplos):**
    * **Archivo JSON (String):** `"examples/scan_results.json"`.
    * **API Key (Variable de Entorno):** `GOOGLE_API_KEY`.
* **Salidas (formatos y ejemplos):**
    * **Formato:** Archivo Markdown (`.md`).
    * **Ejemplo:** `examples/executive_summary_[timestamp].md`.
* **Descripción del procedimiento (narración objetiva de las transformaciones):** El orquestador `run_pipeline.ps1` invoca `src/reporting/ai_summary.py`. Este script lee la API key desde el entorno. Carga el `scan_results.json` y lo inserta en un prompt cargado desde `prompts/prompt_v1.json`. Utiliza `google-generativeai` para llamar al modelo, implementando una lógica de reintentos (`try...except` con `time.sleep`) para manejar fallos de API. La respuesta de texto de la IA se guarda en un archivo `.md` con marca de tiempo.
* **Complejidad técnica (qué de las dimensiones listadas usa la tarea):**
    * Uso de una librería especializada (`google-generativeai`).
    * Procesamiento/parsing de salidas (transforma de `JSON` a `Markdown` via IA).
    * Correlación mínima (conecta el resultado del escaneo con un análisis de IA).
* **Artefactos de evidencia entregados (rutas dentro del repo):**
    * `src/reporting/ai_summary.py`
    * `prompts/prompt_v1.json`
    * `examples/executive_summary_...md`
* **Riesgos y controles éticos (cómo se mitigaron):** El riesgo principal es la fuga de la API key. Se mitiga cargándola *solo* desde una variable de entorno. El orquestador `run_pipeline.ps1` maneja la clave de forma segura (`-AsSecureString`) y la guarda en un archivo que está en el `.gitignore`.
* **Dependencias (comandos, librerías, variables de entorno):**
    * Librería Python: `google-generativeai`.
    * Variable de Entorno: `GOOGLE_API_KEY`.