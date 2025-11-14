## 📌 **AI Plan – RedScan-Py**

Este documento describe el plan de integración de Inteligencia Artificial dentro del proyecto **RedScan-Py**, correspondiente al Entregable 3. Se explican los objetivos, metodología, flujo del sistema, componentes, análisis basado en IA y limitaciones actuales.

---

# 🧠 **1. Objetivo del sistema con IA**

El objetivo del componente de Inteligencia Artificial en RedScan-Py es:

* Analizar los resultados del escaneo de red.
* Detectar patrones inusuales o riesgos potenciales.
* Clasificar el nivel de riesgo de los dispositivos descubiertos.
* Generar un resumen claro y entendible para el usuario final.
* Crear un archivo JSON/Markdown con recomendaciones automáticas.

Esta IA **no toma decisiones automáticas**, solo brinda un análisis descriptivo e informativo.

# 🔁 **2. Flujo del pipeline IA**

1. **scanner.py**

   * Obtiene IP del usuario.
   * Escanea la red usando ping o ARP.
   * Genera un archivo `scan_results.json`.

2. **run_pipeline.sh**

   * Llama a `scanner.py` y valida errores.
   * Registra logs por módulo.
   * Llama a `ai_summary.py`.

3. **ai_summary.py**

   * Lee el JSON del escaneo.
   * Analiza patrones (cantidad de hosts, comportamiento, rangos).
   * Clasifica riesgo: *bajo, medio o alto*.
   * Genera un archivo `ai_summary.md`.

4. **logs.jsonl**

   * Guarda eventos de cada fase:

     * timestamp
     * run_id
     * módulo
     * nivel de severidad
     * descripción

---

# 🔍 **3. Funcionalidad del análisis con IA**

El módulo `ai_summary.py` utiliza un modelo local basado en heurísticas + estructura tipo LLM simulada:

### ✔ patrones detectados:

* Cantidad total de hosts
* Hosts activos/inactivos
* Direcciones IP fuera de rango
* Patrones sospechosos como:

  * direcciones duplicadas
  * dispositivos con respuesta lenta
  * MAC desconocidas
  * posibles intrusos

### ✔ clasificación de riesgo:

* **Bajo:** pocos hosts, todos conocidos, sin anomalías.
* **Medio:** hosts desconocidos o tiempos de respuesta elevados.
* **Alto:** múltiples anomalías → posible intruso.

### ✔ salida generada:

* `ai_summary.md` para el usuario
* texto claro y entendible
* recomendaciones automáticas

---

# 📄 **4. Modelo de datos**

## Entrada → `scan_results.json`

```json
{
  "network": "192.168.1.0/24",
  "devices": [
    {
      "ip": "192.168.1.1",
      "latency": 12,
      "status": "up"
    }
  ]
}
```

## Salida → `ai_summary.md`

* Resumen del escaneo
* Niveles de riesgo
* Explicación de patrones
* Recomendaciones

---

# 🔒 **5. Consideraciones éticas del uso de IA**

* El sistema **no adivina información personal**.
* La IA solo analiza datos suministrados por el usuario.
* No se automatizan medidas invasivas (bloqueos, escaneos agresivos).
* El modelo debe ser usado únicamente en redes donde el usuario tiene permiso.

---

# ⚠️ **6. Limitaciones y siguientes mejoras**

### Limitaciones actuales:

* El análisis IA es descriptivo, no predictivo.
* No usa modelos LLM reales por limitación de API Key.
* No detecta vulnerabilidades en tiempo real.

### Mejoras previstas:

* Integración con API (Shodan, HaveIBeenPwned si se obtiene key).
* Reportes PDF automáticos.
* Sistema de detección de intrusos ligero (IDS).
* Dashboard web en Flask.

---

# 📌 **7. Conclusión**

El componente de IA del proyecto RedScan-Py agrega la capacidad de interpretar los datos obtenidos durante el escaneo y producir un análisis útil para el usuario final. Este análisis, aunque no es un sistema avanzado de machine learning, cumple con el propósito académico del Entregable 3: integrar IA funcional dentro de un pipeline automatizado.
