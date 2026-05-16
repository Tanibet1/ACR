import selectors
import socket
import time
import logging

# Configuracion del log con hora, nivel y mensaje
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Parametros del servidor
HOST = "127.0.0.1"
PORT = 65432
TIMEOUT_INACTIVIDAD = 15  # segundos sin datos para considerar sensor inactivo
INTERVALO_LIMPIEZA  = 5   # cada cuantos segundos se revisan timeouts

# Selector: detecta que sockets tienen datos listos sin bloquear
sel = selectors.DefaultSelector()

# Diccionario de sensores: sensor_id
sensores_activos: dict[str, dict] = {}

# Buffer por socket: acumula datos parciales hasta recibir '\n'
buffers: dict[socket.socket, bytes] = {}


def contar_activos() -> int:
    return len(sensores_activos)


def registrar_evento(mensaje: str) -> None:
    # Imprime un evento con el numero de sensores activos en ese momento
    logger.info("%s | Sensores activos: %d", mensaje, contar_activos())


def desconectar_sensor(conn: socket.socket, razon: str = "desconexión") -> None:
    # Busca el sensor_id que corresponde a este socket
    sensor_id = next(
        (sid for sid, info in sensores_activos.items() if info["conn"] is conn),
        None
    )

    # Quita el socket del selector y lo cierra
    try:
        sel.unregister(conn)
    except Exception:
        pass

    try:
        conn.close()
    except Exception:
        pass

    # Limpia el buffer y elimina el sensor de la lista
    buffers.pop(conn, None)

    if sensor_id:
        del sensores_activos[sensor_id]
        registrar_evento(f"Sensor '{sensor_id}' eliminado por {razon}")
    else:
        registrar_evento(f"Cliente desconocido eliminado por {razon}")


def aceptar_conexion(sock_servidor: socket.socket) -> None:
    # Acepta la nueva conexion y la pone en modo no bloqueante
    conn, addr = sock_servidor.accept()
    conn.setblocking(False)

    # Registra el sensor con la IP:puerto como id temporal
    id_temp = f"{addr[0]}:{addr[1]}"
    sensores_activos[id_temp] = {
        "conn": conn,
        "addr": addr,
        "ultimo_dato": time.time(),
    }
    buffers[conn] = b""

    # Registra el socket en el selector para escuchar lectura
    sel.register(conn, selectors.EVENT_READ, data=leer_datos)
    registrar_evento(f"Nueva conexión desde {addr} (id temporal: '{id_temp}')")


def leer_datos(conn: socket.socket) -> None:
    try:
        fragmento = conn.recv(1024)
    except ConnectionResetError:
        desconectar_sensor(conn, "error de conexión")
        return

    if not fragmento:
        # El cliente cerro la conexion limpiamente
        desconectar_sensor(conn, "cierre limpio")
        return

    # Acumula el fragmento en el buffer del socket
    buffers[conn] += fragmento

    # Procesa todas las lineas completas disponibles
    while b"\n" in buffers[conn]:
        linea, buffers[conn] = buffers[conn].split(b"\n", 1)
        linea = linea.strip()
        if linea:
            procesar_mensaje(conn, linea.decode("utf-8", errors="replace"))


def procesar_mensaje(conn: socket.socket, mensaje: str) -> None:
    # Espera el formato: sensor_id,valor
    partes = mensaje.split(",", 1)
    if len(partes) != 2:
        logger.warning("Formato incorrecto: '%s'", mensaje)
        return

    sensor_id, valor = partes[0].strip(), partes[1].strip()

    # Si llega el primer mensaje, reemplaza el id temporal por el real
    id_temp = next(
        (sid for sid, info in sensores_activos.items() if info["conn"] is conn),
        None
    )
    if id_temp and id_temp != sensor_id:
        info = sensores_activos.pop(id_temp)
        sensores_activos[sensor_id] = info
        logger.info("Sensor identificado: '%s' (antes '%s')", sensor_id, id_temp)

    # Actualiza el timestamp de ultima actividad
    if sensor_id in sensores_activos:
        sensores_activos[sensor_id]["ultimo_dato"] = time.time()

    print(f"Sensor {sensor_id} reporta: {valor}")


def limpiar_inactivos() -> None:
    # Revisa todos los sensores y desconecta los que superaron el timeout
    ahora = time.time()
    inactivos = [
        (sid, info)
        for sid, info in list(sensores_activos.items())
        if ahora - info["ultimo_dato"] > TIMEOUT_INACTIVIDAD
    ]
    for sid, info in inactivos:
        logger.warning("Sensor '%s' inactivo por más de %ds", sid, TIMEOUT_INACTIVIDAD)
        desconectar_sensor(info["conn"], "timeout de inactividad")


def iniciar_servidor() -> None:
    # Crea el socket TCP y lo pone a escuchar
    sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_servidor.bind((HOST, PORT))
    sock_servidor.listen()
    sock_servidor.setblocking(False)

    # Registra el socket servidor para detectar nuevas conexiones
    sel.register(sock_servidor, selectors.EVENT_READ, data=aceptar_conexion)
    logger.info("Servidor escuchando en %s:%d", HOST, PORT)
    logger.info("Timeout de inactividad: %ds | Revisión cada %ds",
                TIMEOUT_INACTIVIDAD, INTERVALO_LIMPIEZA)

    ultima_limpieza = time.time()

    try:
        while True:
            # Espera hasta que algun socket este listo (max. INTERVALO_LIMPIEZA seg)
            eventos = sel.select(timeout=INTERVALO_LIMPIEZA)

            for clave, mascara in eventos:
                callback = clave.data
                callback(clave.fileobj)  # llama a aceptar_conexion o leer_datos

            # Cada INTERVALO_LIMPIEZA segundos revisa sensores inactivos
            if time.time() - ultima_limpieza >= INTERVALO_LIMPIEZA:
                limpiar_inactivos()
                ultima_limpieza = time.time()

    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario (Ctrl+C).")
    finally:
        sel.close()
        sock_servidor.close()
        logger.info("Recursos liberados.")


if __name__ == "__main__":
    iniciar_servidor()