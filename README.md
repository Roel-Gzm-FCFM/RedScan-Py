# RedScan-Py: Escáner de Autenticación en Red Local

## 📌 Descripción General del Proyecto

**RedScan-Py** es una herramienta de auditoría de seguridad desarrollada en Python, diseñada para automatizar la revisión básica de seguridad en redes locales (LAN).

El propósito principal del proyecto es:

* **Identificar dispositivos activos** dentro de una subred.
* **Evaluar configuraciones SSH** mediante pruebas controladas en el puerto 22.
* **Detectar credenciales débiles o por defecto** para identificar configuraciones inseguras.

El proyecto forma parte del área de **Red Team / Pentesting**, simulando un escenario real de reconocimiento y fuerza bruta autorizada dentro de un entorno controlado.

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

La herramienta **no almacena credenciales exitosas**, no realiza acciones de post-explotación y emplea contraseñas sintéticas de dominio público.
El equipo no se responsabiliza por el uso indebido de este software.

---

## 📂 Estructura del Proyecto

```
RedScan-Py/
└── src/
│    └── Tarea2_check_ssh.py              # Función principal para pruebas SSH
│    └── runs_scan.py           
│    └── ai_summary.py             # Integración con Google Gemini
│    └── main.py                   # Orquestación del flujo
│
├── scripts/
│   └── run_pipeline.sh       # Script para ejecutar todo el proceso
│
├── prompts/
│   └── prompt_v1.json        # Prompt base de IA
│
├── examples/
│   ├── logs.jsonl            # Logs generados (JSON Lines)
│   ├── ai_output.json        # Salida generada por la IA
│   └── scan_results.json     # Resultados del escaneo
│   └── test_check_ssh.py     # Evidencia de funcionamiento
│
├── docs/
│   ├── propuesta.md          # Documento técnico inicial
│   ├── ai_plan.md            # Plan de integración de IA
│   └── entregable_2.md       
│   └── entregable_3.md
│   └── entregable_4.md   
```

---

## 🔧 Ejecución del Proyecto

### **1️⃣ Instalar dependencias**

```bash
pip install -r requirements.txt
```

### **2️⃣ Dar permisos al script (Linux/Mac)**

```bash
chmod +x scripts/run_pipeline.sh
```

### **3️⃣ Ejecutar el pipeline completo**

```bash
./scripts/run_pipeline.sh
```

Este script ejecuta **todo el flujo técnico**, incluyendo:

1. Escaneo de red
2. Pruebas SSH
3. Logging estructurado
4. Llamada a IA (Gemini)
5. Generación del resumen final

---

## 🤖 Integración de IA

Se incorporó inteligencia artificial para análisis automático de riesgos de seguridad.
La IA genera:

* Resúmenes de hallazgos
* Identificación de patrones
* Recomendaciones técnicas
* Evaluación de exposición de la red

### Implementación incluida

* `ai_summary.py` → Implementación de Google Gemini
* Prompt en `prompts/prompt_v1.json`
* Salida guardada en `/examples/ai_output.json`
* Orquestación automática desde `run_pipeline.sh`
* Logging estructurado en `.jsonl`
