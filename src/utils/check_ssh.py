import paramiko
import socket
import json
import time

def check_ssh(ip, usuario, password, log_path=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    resultado = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ip": ip,
        "usuario": usuario,
        "exito": False
    }

    try:
        client.connect(hostname=ip, username=usuario, password=password, timeout=5)
        resultado["exito"] = True
    except paramiko.AuthenticationException:
        resultado["error"] = "Autenticación fallida"
    except (paramiko.SSHException, socket.timeout, socket.error) as e:
        resultado["error"] = str(e)
    finally:
        client.close()
        if log_path:
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(json.dumps(resultado) + "\n")
        return resultado["exito"]
