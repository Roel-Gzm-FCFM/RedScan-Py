# Entregable 2 – Avance Técnico del Proyecto RedScan-Py

## ✅ Tarea funcional implementada

Se ha implementado la **Tarea 2: Verificación de Credenciales Débiles (Fuerza Bruta SSH)**, correspondiente al módulo de autenticación del proyecto. Esta tarea permite probar combinaciones de usuario y contraseña contra dispositivos activos en la red local mediante el protocolo SSH.

- **Archivo fuente**: `/src/check_ssh.py`
- **Función principal**: `check_ssh(ip, usuario, password, log_path=None)`
- **Librería utilizada**: `paramiko`

---

## ⚙️ Entradas y salidas

### Entradas esperadas:
- `ip` (str): Dirección IP del host objetivo.
- `usuario` (str): Nombre de usuario a probar.
- `password` (str): Contraseña a probar.
- `log_path` (str, opcional): Ruta del archivo de log en formato JSON Lines.

### Salida esperada:
- `True` si la conexión SSH fue exitosa.
- `False` si falló por cualquier motivo (credenciales incorrectas, timeout, conexión rehusada, etc.).

---

## 🧪 Evidencia de ejecución

Se ha creado el script `/examples/test_check_ssh.py` que ejecuta la función `check_ssh` con múltiples combinaciones de IPs, usuarios y contraseñas.

### Archivos generados:
- `/examples/ssh_log.jsonl`: Archivo de log estructurado en formato JSON Lines.
- Salida por consola con mensajes de éxito o fallo por cada intento de conexión.

### Ejemplo de línea en el log:
```json
{"timestamp": "2025-11-08T17:05:00", "ip": "192.168.1.50", "usuario": "pi", "exito": true}
