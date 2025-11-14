# RedScan-Py: Escáner de Autenticación Local

## 📌 Descripción General del Proyecto

**RedScan-Py** es una herramienta de auditoría de seguridad desarrollada en Python y orquestada con PowerShell, diseñada para automatizar la revisión de seguridad básica en la máquina local.

El propósito principal del proyecto es:

* **Auto-descubrimiento:** Identificar la dirección IP local activa de la máquina.
* **Auto-evaluación:** Evaluar la configuración SSH de la propia máquina (probando en `localhost` o la IP detectada) mediante pruebas controladas.
* **Detección de Credenciales:** Usar una lista de credenciales débiles para verificar if el servicio SSH es vulnerable.

El proyecto forma parte del área de **Red Team / Pentesting**, simulando un escenario de auto-auditoría para identificar configuraciones inseguras antes de que sean explotadas.

---

## ⚖️ Declaración Ética y Legal

Este software fue desarrollado con fines **académicos y educativos**, dentro del Producto Integrador de Aprendizaje (PIA) de la materia *Programación para Ciberseguridad*.

### ✔ Uso permitido

* Laboratorios personales
* Redes privadas propias
* Sistemas donde exista **autorización explícita**

### ❌ Prohibido

* Redes corporativas
* Redes públicas
* Sistemas de terceros sin permiso por escrito

El equipo no se responsabiliza por el uso indebido de este software.

---

## 📂 Estructura del Proyecto

```

RedScan-Py/
├── docs/
│   ├── ai\_plan.md            \# Plan de integración de IA
│   ├── entregable\_2.md
│   ├── entregable\_3.md
│   └── entregable\_4.md       \# Avance más reciente
├── examples/
│   ├── logs.jsonl            \# Logs generados (JSON Lines)
│   ├── scan\_results.json     \# Resultados del escaneo (Tarea 1)
│   └── executive\_summary.md  \# Reporte de IA (Tarea 2)
├── prompts/
│   └── prompt\_v1.json        \# Prompt base de IA
├── scripts/
│   └── run\_pipeline.ps1      \# Orquestador principal (PowerShell)
├── src/
│   ├── acquisition/          \# Tarea 1: Adquisición de datos
│   │   └── run\_scan.py
│   ├── reporting/            \# Tarea 2: Reporte con IA
│   │   └── ai\_summary.py
│   └── utils/                \# Módulos de apoyo
│       └── check\_ssh.py
├── .gitignore
├── README.md                 \# Este archivo
└── requirements.txt          \# Dependencias de Python

````

---

## 🔧 Ejecución del Proyecto (Windows)

Este proyecto está diseñado para ejecutarse en un entorno **Windows** con **PowerShell**.

### **1️⃣ Instalación (Solo la primera vez)**

Desde la raíz del proyecto, ejecuta los siguientes comandos en PowerShell:

```powershell
# 1. Crea el entorno virtual (una carpeta .venv)
python -m venv .venv

# 2. Activa el entorno
.\.venv\Scripts\Activate.ps1

# 3. Instala todas las dependencias de Python
pip install -r requirements.txt
````

### **2️⃣ Ejecución Normal (Pipeline Completo)**

Una vez instalado, solo necesitas hacer esto cada vez que quieras ejecutarlo:

```powershell
# 1. Activa el entorno (si no está activo)
.\.venv\Scripts\Activate.ps1

# 2. Navega a la carpeta de scripts
cd scripts

# 3. Ejecuta el pipeline
powershell.exe -ExecutionPolicy Bypass -File .\run_pipeline.ps1
```

Este script ejecuta **todo el flujo técnico**:

1.  **Solicitud de API:** Te preguntará por tu API Key de Google Gemini si no la encuentra guardada.
2.  **Escaneo (Python):** Ejecuta `src/acquisition/run_scan.py` para detectar la IP local y probar las credenciales SSH.
3.  **Análisis (Python):** Ejecuta `src/reporting/ai_summary.py` para enviar los resultados a la IA.
4.  **Logging (PowerShell):** Registra todos los pasos en `examples/logs.jsonl`.
5.  **Reporte (IA):** Genera un resumen final en `examples/executive_summary.md`.

-----

## 🤖 Integración de IA

Se incorporó inteligencia artificial para el análisis de los resultados del escaneo. La IA (Google Gemini) se utiliza para:

  * Resumir los hallazgos del escaneo (éxitos o fracasos).
  * Proveer un análisis simple de la postura de seguridad.

### Implementación incluida

  * `src/reporting/ai_summary.py` → Módulo que se conecta a la API de Google Gemini.
  * `prompts/prompt_v1.json` → Plantilla del prompt enviado a la IA.
  * `scripts/run_pipeline.ps1` → Orquestador que llama al script de IA y maneja la API key de forma interactiva.
  * **Manejo de Errores:** El script de IA incluye reintentos (`retries`) para manejar fallos temporales de la API.
