"""
Ejercicio 2.6 - Parte 2: Servidor UDP
No hay conexión: cada mensaje trae la dirección del cliente.
La demultiplexación es implícita: el SO usa (IP, puerto) para identificar al remitente.
"""

import socket

HOST = "127.0.0.1"
PORT = 65002

# Asocia (IP, puerto) con el ID_CLIENTE del mensaje
clientes: dict[tuple, str] = {}


def calcular(operacion: str, valor: int) -> str:
    if operacion == "SQR":
        return str(valor ** 2)
    elif operacion == "CUBE":
        return str(valor ** 3)
    elif operacion == "NEG":
        return str(-valor)
    else:
        return "ERROR:OPERACION_INVALIDA"


def procesar_mensaje(mensaje: str) -> str:
    partes = mensaje.strip().split(":")
    if len(partes) != 3:
        return "ERROR:FORMATO_INVALIDO"

    cliente_id, operacion, valor_str = partes

    try:
        valor = int(valor_str)
    except ValueError:
        return f"{cliente_id}:ERROR:VALOR_NO_ENTERO"

    resultado = calcular(operacion, valor)
    return f"{cliente_id}:{resultado}"


def iniciar_servidor():
    # Un solo socket UDP atiende a todos los clientes
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))
    print(f"[UDP] Servidor escuchando en {HOST}:{PORT}")

    try:
        while True:
            # recvfrom devuelve los datos Y la dirección del remitente
            # — aquí ocurre la demultiplexación implícita: la capa de
            #   transporte entrega junto con el mensaje quién lo envió
            datos, addr = servidor.recvfrom(1024)
            mensaje = datos.decode("utf-8", errors="replace").strip()
            print(f"[UDP] Recibido de {addr}: '{mensaje}'")

            # Registra o actualiza el ID_CLIENTE asociado a esa dirección
            partes = mensaje.split(":")
            if len(partes) == 3:
                clientes[addr] = partes[0]

            respuesta = procesar_mensaje(mensaje)
            print(f"[UDP] Respuesta a {addr}: '{respuesta}'")

            # Responde usando la dirección que devolvió recvfrom
            servidor.sendto((respuesta + "\n").encode(), addr)

    except KeyboardInterrupt:
        print("\n[UDP] Servidor detenido.")
    finally:
        servidor.close()


if __name__ == "__main__":
    iniciar_servidor()