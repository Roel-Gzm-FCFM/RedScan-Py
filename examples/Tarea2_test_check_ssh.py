# examples/Tarea2_test_check_ssh.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Tarea2_check_ssh import check_ssh

# IPs de ejemplo (ajusta con IPs reales de tu red si quieres)
pruebas = [
    ("192.168.1.10", "admin", "1234"),
    ("192.168.1.11", "root", "toor"),
]

log_path = r"C:\Users\bitog\Desktop\RedScan-Py\examples\ssh_log.jsonl"

for ip, user, pwd in pruebas:
    resultado = check_ssh(ip, user, pwd, log_path=log_path)
    print(f"{ip} → {'✔️ Conectado' if resultado else '❌ Falló'}")
