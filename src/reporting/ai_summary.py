import json
import os
import sys
import datetime
import time

try:
    import google.generativeai as genai
except Exception as e:
    print("ERROR: falta la librería google-generativeai. Instala con: pip install google-generativeai")
    sys.exit(1)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("ERROR: No se encontró la variable de entorno GOOGLE_API_KEY.")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# --- INICIO: Lógica de Reintentos (Requisito del PIA) ---
def llamar_api_con_reintentos(model, prompt, intentos=3):
    """
    Llama a la API de Gemini con una política de reintentos simple.
    """
    for i in range(intentos):
        try:
            print(f"[IA] Solicitando análisis a Gemini (Intento {i+1}/{intentos})...")
            # Inicia la generación de contenido
            response = model.generate_content(prompt)
            # Espera a que la respuesta se complete y retorna el texto
            return response.text.strip() 
        except Exception as e:
            print(f"[IA] ERROR: Intento {i+1} falló.")
            print(f"[DEBUG] {e}")
            if i < intentos - 1: # Si no es el último intento
                print("[IA] Esperando 5 segundos para reintentar...")
                time.sleep(5) # Espera 5 segundos (Backoff simple)
            else:
                print("[IA] Todos los intentos fallaron.")
                # Lanza el error para que el pipeline de PowerShell lo capture
                raise e 
# --- FIN: Lógica de Reintentos ---

def analizar_resultados(scan_file):
    try:
        with open(scan_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error al leer el archivo {scan_file}: {e}")
        sys.exit(1)

    prompt = (
        "Eres un asistente experto en ciberseguridad. Analiza los siguientes resultados de escaneo "
        "y genera un resumen breve en formato Markdown: servicios expuestos, hosts con éxito de autenticación y recomendaciones.\n\n"
        f"{json.dumps(data, indent=2)}"
    )

    # Usamos el modelo gemini-2.0-flash-lite (el que te funcionó)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    
    try:
        # Usamos la nueva función con reintentos
        output_text = llamar_api_con_reintentos(model, prompt)
    except Exception as e:
        # El error ya fue impreso por la función de reintentos, solo salimos
        sys.exit(1)

    # --- INICIO: Guardado de Reporte ---
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"examples/executive_summary_{timestamp}.md" 
    
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(output_text)

    # --- FIN: Guardado de Reporte ---

    print(f"[IA] Resumen ejecutivo guardado en: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/ai_summary.py <examples/scan_results.json>")
        sys.exit(1)
    
    # Asegúrate de que la carpeta /examples exista (igual que en run_scan.py)
    os.makedirs("examples", exist_ok=True)
    
    analizar_resultados(sys.argv[1])