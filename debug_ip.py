import subprocess

salida = subprocess.check_output("ipconfig", text=True, encoding="utf-8", errors="ignore")

print("=== Líneas de salida ===")
for i, linea in enumerate(salida.splitlines()):
    print(f"{i}: '{linea}'")
    if "IPv4" in linea or "Dirección" in linea:
        print(f"  -> Contiene IPv4/Dirección")
    if "Máscara" in linea or "subred" in linea:
        print(f"  -> Contiene Máscara/subred")
    if "Puerta" in linea or "Gateway" in linea:
        print(f"  -> Contiene Puerta/Gateway")
