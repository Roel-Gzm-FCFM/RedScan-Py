# src/ai_summary.py
import json
import os
import sys
import datetime

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

def analizar_resultados(scan_file):
    try:
        with open(scan_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error al leer el archivo {scan_file}: {e}")
        sys.exit(1)

    prompt = (
        "Eres un asistente experto en ciberseguridad. Analiza los siguientes resultados de escaneo "
        "y genera un resumen breve: servicios expuestos, hosts con éxito de autenticación y recomendaciones.\n\n"
        f"{json.dumps(data, indent=2)}"
    )

    # Usamos el modelo gemini-1.5-flash (ajusta si usas otro)
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        print(f"Error al llamar al API de Gemini: {e}")
        sys.exit(1)

    # response puede tener texto en data; aquí usamos la forma simple
    # según la SDK, response.text es lo que queremos
    output_text = getattr(response, "text", None)
    if output_text is None:
        # intentar otras rutas de la respuesta
        try:
            output_text = response.candidates[0].content[0].text
        except Exception:
            output_text = json.dumps(response.__dict__, default=str)

    output_text = output_text.strip()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.abspath(f"examples/ai_summary_{timestamp}.txt")
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(output_text)

    # registrar también en logs.jsonl
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "module": "ai_summary",
        "level": "INFO",
        "event": "AI analysis done",
        "details": {"output_file": out_path}
    }
    with open("examples/logs.jsonl", "a", encoding="utf-8") as logf:
        logf.write(json.dumps(log_entry) + "\n")

    print("[ai] Análisis completado.")
    print(f"[ai] Resumen guardado en: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/ai_summary.py <examples/scan_results.json>")
        sys.exit(1)
    analizar_resultados(sys.argv[1])
