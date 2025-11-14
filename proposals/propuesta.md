# Propuesta Técnica: RedScan-Py

## 1. Título del Proyecto
RedScan-Py: Escáner de Vulnerabilidades de Autenticación en Red Local

## 2. Descripción General del Proyecto
Herramienta de línea de comandos escrita en Python para automatizar la auditoría de redes locales. Su propósito es identificar dispositivos activos y evaluar su postura de seguridad en el servicio SSH (puerto 22) intentando acceder mediante credenciales comúnmente usadas o débiles. El enfoque combina reconocimiento de red y pruebas de penetración básicas.

## 3. Fichas Técnicas de Tareas

A continuación, se detallan las dos tareas principales que compondrán el núcleo funcional de la herramienta.

---

### Ficha Técnica: Tarea 1

* **Título y Propósito:**
    Tarea 1: Descubrimiento de Hosts (Reconocimiento de Red).
    Identificar qué direcciones IP dentro de un rango de red local específico están actualmente activas y en línea.
* **Función / Rol de Ciberseguridad:**
    Red Team (Fase de Reconocimiento) y Blue Team (Gestión de Activos / Visibilidad de Red).
* **Entradas Esperadas:**
    * **Formato:** Cadena de texto (string).
    * **Ejemplo:** Un rango de red en formato CIDR, como `"192.168.1.0/24"`.
* **Salidas Esperadas:**
    * **Formato:** Una lista de direcciones IP activas.
    * **Ejemplo:** `['192.168.1.1', '192.168.1.50', '192.168.1.104']`. Esta lista será consumida por la Tarea 2.
* **Descripción del Procedimiento:**
    El script construirá y enviará paquetes ARP (Address Resolution Protocol) a la dirección de *broadcast* de la subred especificada. Escuchará activamente las respuestas ARP ("is-at") para mapear las direcciones MAC a las direcciones IP, identificando con precisión qué hosts están "vivos" en la red.
* **Complejidad Técnica:**
    Media. Implica la construcción, envío y recepción de paquetes de red de bajo nivel (Capa 2), lo cual requiere privilegios elevados (sudo/admin) para interactuar con el socket crudo.
* **Controles Éticos:**
    La herramienta debe notificar al usuario que este escaneo puede generar "ruido" en la red. Solo debe ejecutarse en redes propias o con permiso explícito del administrador de la red (ej. laboratorios de la universidad).
* **Dependencias:**
    * Python 3.x
    * Librería `scapy`

---

### Ficha Técnica: Tarea 2

* **Título y Propósito:**
    Tarea 2: Verificación de Credenciales Débiles (Fuerza Bruta SSH).
    Probar la robustez de la autenticación SSH en los hosts descubiertos, intentando iniciar sesión con una lista predefinida de usuarios y contraseñas comunes.
* **Función / Rol de Ciberseguridad:**
    Red Team (Fase de Explotación / Obtención de Acceso) y Pentesting.
* **Entradas Esperadas:**
    * **Formato:** La lista de IPs (salida de la Tarea 1). Dos archivos de texto (`.txt`): uno con nombres de usuario (ej. `users.txt`) y otro con contraseñas (ej. `pass.txt`).
    * **Ejemplo:** `users.txt` (Contiene: "root", "admin", "pi") y `pass.txt` (Contiene: "123456", "password", "admin").
* **Salidas Esperadas:**
    * **Formato:** Mensajes en la consola y/o un archivo de reporte (`reporte.txt`).
    * **Ejemplo:** `¡ÉXITO! -> 192.168.1.50 | Usuario: pi | Pass: 123456`
* **Descripción del Procedimiento:**
    El script principal iterará sobre cada IP activa. Para cada IP, intentará establecer una conexión SSH (puerto 22). Utilizará un bucle anidado para probar sistemáticamente cada combinación de usuario y contraseña de los diccionarios. Se manejarán las excepciones comunes (conexión rehusada, autenticación fallida, *timeout*) para continuar con la siguiente combinación. Si una conexión es exitosa, se registrará inmediatamente en la salida.
* **Complejidad Técnica:**
    Media. Requiere el manejo de conexiones de red (sockets), gestión de múltiples hilos (para velocidad, opcional) y un manejo robusto de errores y excepciones de autenticación.
* **Controles Éticos:**
    Crítico. Esta es la parte más sensible. Las credenciales descubiertas **NUNCA** deben usarse para acceder o modificar el sistema. El propósito es solo *reportar* la vulnerabilidad. La herramienta no debe guardar las contraseñas exitosas en un formato que no sea el reporte final, y debe advertir al usuario sobre la legalidad de sus acciones.
* **Dependencias:**
    * Python 3.x
    * Librería `paramiko` (para la conexión SSH)

## 4. Estructura Inicial del Repositorio

Se propone la siguiente estructura de carpetas para organizar el proyecto:

/RedScan-Py/
├── /proposals/
│   └── propuesta.md    (Este documento)
│
├── /src/
│   ├── ssh_scanner.py    (Script principal que ejecuta Tarea 1 y 2)
│   ├── users.txt         (Diccionario de usuarios)
│   └── pass.txt          (Diccionario de contraseñas)
│
├── /docs/
│   └── (Espacio para manual de usuario o documentación técnica)
│
├── /examples/
│   └── reporte_ejemplo.txt (Ejemplo de cómo se verá una salida exitosa)
│
├── README.md             (Descripción del proyecto y Declaración Ética)
└── .gitignore            (Para ignorar archivos como pycache o claves)

## 5. Asignación de Roles y Tareas del Proyecto

* **MORALES MEDINA, GILBERTO (Especialista - Módulo 1: Reconocimiento)**
    * **Tarea Principal:** Desarrollar la función de **escaneo ARP (Tarea 1)**.
    * **Entregable:** Un script o función de Python (usando `scapy`) que reciba un rango de red (ej. "192.168.1.0/24") y **devuelva una lista** de las direcciones IP que están activas.
    * **Responsabilidad:** Asegurar que el escaneo funcione y sea preciso, manejando los permisos de administrador (sudo/admin) que `scapy` pueda necesitar.

* **Guzman Martinez, Roel Antonio (Líder de Proyecto / Integrador)**
    * **Tarea Principal:** Desarrollar el script principal (`ssh_scanner.py`) e **integrar** el trabajo de todos.
    * **Entregable:** El script final que:
        1.  Llama a la función de Gilberto (Tarea 1) para obtener las IPs.
        2.  Lee los archivos de Axel (`users.txt`, `pass.txt`).
        3.  Usa la función de Emiliano (Tarea 2) dentro de un bucle para probar las credenciales en cada IP.
        4.  Imprime el reporte final en la consola.
    * **Responsabilidad:** Gestión del repositorio de GitHub (commits, merges) y asegurar que el proyecto final funcione como un todo.

* **QUEZADA ANTONIO, GUILLERMO (Documentación y Control de Calidad)**
    * **Tarea Principal:** Responsable de toda la documentación del proyecto y la entrega final.
    * **Entregable:**
        1.  Finalizar y pulir el archivo `README.md` con la descripción final, instrucciones de uso y la Declaración Ética.
        2.  Revisar la `propuesta.md` para consistencia.
        3.  Preparar el video o capturas de pantalla para la entrega en MS Teams.

* **FLORES MOLINA, AXEL ALEJANDRO (QA y Recursos de Ataque)**
    * **Tarea Principal:** Crear los diccionarios de ataque y realizar las pruebas de calidad (QA).
    * **Entregable:**
        1.  Los archivos `users.txt` y `pass.txt`, investigando y poblándolos con las credenciales más comunes.
        2.  Probar el script final (`ssh_scanner.py`) en un entorno de laboratorio para encontrar y reportar bugs.
    * **Responsabilidad:** Confirmar que los hallazgos del script son correctos (sin falsos positivos).

* **VILLARREAL SARACCO, EMILIANO (Especialista - Módulo 2: Autenticación)**
    * **Tarea Principal:** Desarrollar la función de **verificación SSH (Tarea 2)**.
    * **Entregable:** Una función de Python (usando `paramiko`) que reciba **tres argumentos** (una IP, un usuario, una contraseña) y **devuelva `True` si la conexión fue exitosa, o `False` si falló**.

    * **Responsabilidad:** Manejar correctamente los errores comunes de `paramiko` (ej. conexión rehusada, autenticación fallida, *timeout*) para que el script de Roel no se detenga.


## 6. Documentacion tecnica avanzada

### Función: check_ssh(ip, usuario, password, log_path=None)
- **Ubicación**: `/src/check_ssh.py`
- **Descripción**: Intenta establecer una conexión SSH usando `paramiko`.
- **Parámetros**:
  - `ip` (str): Dirección IP del host.
  - `usuario` (str): Nombre de usuario.
  - `password` (str): Contraseña.
  - `log_path` (str, opcional): Ruta del archivo de log en formato JSON Lines.
- **Retorno**: `True` si la conexión fue exitosa, `False` si falló.
- **Excepciones manejadas**: `AuthenticationException`, `SSHException`, `socket.timeout`, `socket.error`.
- **Formato de log**: JSON Lines con campos `timestamp`, `ip`, `usuario`, `exito`, `error` (si aplica).
