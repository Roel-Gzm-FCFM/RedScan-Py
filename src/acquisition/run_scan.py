import sys
import os
import json
import subprocess
import re

# (Importante: Asume que la carpeta 'src' está en 'RedScan-Py-main/src')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.check_ssh import check_ssh

OUTPUT_FILE = "examples/scan_results.json"
USERS_FILE = "users.txt"  # Archivo en la raíz del proyecto
PASS_FILE = "passwords.txt" # Archivo en la raíz del proyecto

# -----------------------------
# Obtener una sola IP del sistema
# -----------------------------
def obtener_ip_simple():
    try:
        # Usamos latin-1 para evitar errores de codificación con 'ipconfig' en español
        salida = subprocess.check_output("ipconfig", text=True, encoding="latin-1")
        patron = r"IPv4.*?:\s*([\d\.]+)"  # Extrae algo como 192.168.1.34
        match = re.search(patron, salida)
        return match.group(1) if match else None
    except Exception as e:
        print(f"[ERROR] No se pudo ejecutar 'ipconfig': {e}")
        return None

# -----------------------------
# Cargar listas desde archivos
# -----------------------------
def cargar_lista(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] No se encontró el archivo: {filename}")
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # .strip() quita los espacios en blanco y saltos de línea
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo {filename}: {e}")
        return []

# -----------------------------
# Escaneo
# -----------------------------
def ejecutar_scan():
    ip_local = obtener_ip_simple()

    if not ip_local:
        print("[ERROR] No se pudo obtener la IP local. Terminando escaneo.")
        return

    print(f"IP detectada automáticamente: {ip_local}")

    # Cargar las listas
    usuarios = cargar_lista(USERS_FILE)
    contrasenas = cargar_lista(PASS_FILE)

    if not usuarios or not contrasenas:
        print("[ERROR] Faltan archivos de usuarios o contraseñas. Terminando.")
        return

    print(f"[*] Listas cargadas: {len(usuarios)} usuarios y {len(contrasenas)} contraseñas.")
    print(f"[*] Se probarán hasta {len(usuarios) * len(contrasenas)} combinaciones contra {ip_local}.")

    resultados = [] # La lista final de resultados
    exito_general = False # Flag para saber si encontramos algo en todo el scan

    # ¡Aquí ocurre la magia! Bucles anidados
    for user in usuarios:
        print(f"--- Probando Usuario: {user} ---")
        encontrado_para_este_usuario = False # Un flag para este usuario

        for pwd in contrasenas:
            print(f"Probando {ip_local} con usuario {user}...")
            
            # Llamamos a la función de Emiliano
            resultado = check_ssh(ip_local, user, pwd)
            
            if resultado:
                print(f"¡ÉXITO! Credenciales encontradas: {user}:{pwd}")
                resultados.append({
                    "ip": ip_local,
                    "usuario": user,
                    "password_encontrado": pwd, # Reporta la contraseña que funcionó
                    "exito": True
                })
                encontrado_para_este_usuario = True # Marcamos que este usuario tuvo éxito
                exito_general = True
                break # Dejamos de probar más contraseñas para ESTE usuario

        # --- CAMBIO IMPORTANTE ---
        # Al terminar el bucle de contraseñas, revisamos si encontramos algo
        # Si NO encontramos nada, registramos el fallo para ESE usuario
        if not encontrado_para_este_usuario:
            print(f"[!] Fallaron todas las contraseñas para el usuario: {user}")
            resultados.append({
                "ip": ip_local,
                "usuario": user,
                "password_encontrado": None,
                "exito": False
            })

    # Bucle 'for user' terminado. Todos los usuarios han sido probados.

    if not exito_general:
        print("[!] No se encontraron credenciales válidas en todo el escaneo.")

    # Guardamos TODOS los resultados (éxitos Y fracasos)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2)

    print(f"Escaneo completado. Resultados guardados en {OUTPUT_FILE}")


if __name__ == "__main__":
    # Asegúrate de que las carpetas existan
    os.makedirs("examples", exist_ok=True)
    os.makedirs("logs", exist_ok=True) # Aunque no se usa aquí, es bueno tenerlo
    
    ejecutar_scan()