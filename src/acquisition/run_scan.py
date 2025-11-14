import sys
import os
import json
import subprocess
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.check_ssh import check_ssh

OUTPUT_FILE = "examples/scan_results.json"

# -----------------------------
# Obtener una sola IP del sistema
# -----------------------------
def obtener_ip_simple():
    salida = subprocess.check_output("ipconfig", text=True, encoding="latin-1")
    patron = r"IPv4.*?:\s*([\d\.]+)"   # Extrae algo como 192.168.1.34
    match = re.search(patron, salida)
    return match.group(1) if match else None

# -----------------------------
# Escaneo
# -----------------------------
def ejecutar_scan():
    ip_local = obtener_ip_simple()

    if not ip_local:
        print("No se pudo obtener la IP local.")
        return

    print(f"IP detectada automáticamente: {ip_local}")

    pruebas = [
        (ip_local, "admin", "1234"),
        (ip_local, "root", "toor")
    ]

    resultados = []

    for ip, user, pwd in pruebas:
        print(f"Probando {ip} con usuario {user}...")
        resultado = check_ssh(ip, user, pwd)
        resultados.append({
            "ip": ip,
            "usuario": user,
            "exito": resultado
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2)

    print(f"Escaneo completado. Resultados guardados en {OUTPUT_FILE}")

if __name__ == "__main__":
    ejecutar_scan()

