import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from run_scan import obtener_red_windows, mascara_a_cidr

ip, mascara = obtener_red_windows()
print(f"IP detectada: {ip}")
print(f"Máscara detectada: {mascara}")

if ip and mascara:
    cidr = mascara_a_cidr(mascara)
    print(f"CIDR: {ip}/{cidr}")
    print("✓ Detección exitosa!")
else:
    print("✗ Error: No se detectó IP o máscara")
