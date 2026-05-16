"""
Ejercicio 2.6 - Parte 1: Servidor TCP con select()
Formato de mensaje: ID_CLIENTE:OPERACION:VALOR
Operaciones: SQR (cuadrado), CUBE (cubo), NEG (cambio de signo)
"""

import select
import socket

HOST = "127.0.0.1"
PORT = 65001

# Asocia cada socket con el ID_CLIENTE que se identificó
clientes: dict[socket.socket, str] = {}


def calcular(operacion: str, valor: int) -> str:
    # Ejecuta la operación y devuelve el resultado como string
    if operacion == "SQR":
        return str(valor ** 2)
    elif operacion == "CUBE":
        return str(valor ** 3)
    elif operacion == "NEG":
        return str(-valor)
    else:
        return "ERROR:OPERACION_INVALIDA"


def procesar_mensaje(mensaje: str) -> str:
    # Valida el formato ID:OP:VALOR y retorna la respuesta
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
    # Crea el socket servidor TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[TCP] Servidor escuchando en {HOST}:{PORT}")

    # Lista de sockets que select() debe vigilar
    entradas = [servidor]

    try:
        while True:
            # select() bloquea hasta que algún socket esté listo para leer
            # — aquí ocurre la demultiplexación: select devuelve exactamente
            #   qué sockets tienen datos, evitando leer de todos a la vez
            listos, _, _ = select.select(entradas, [], [])

            for sock in listos:
                if sock is servidor:
                    # Nuevo cliente: acepta la conexión y lo agrega a la lista
                    conn, addr = servidor.accept()
                    entradas.append(conn)
                    clientes[conn] = None  # ID aún desconocido
                    print(f"[TCP] Nueva conexión desde {addr}")
                else:
                    # Socket existente con datos listos
                    try:
                        datos = sock.recv(1024)
                    except ConnectionResetError:
                        datos = None

                    if not datos:
                        # Cliente desconectado
                        cid = clientes.get(sock, "desconocido")
                        print(f"[TCP] Cliente '{cid}' desconectado")
                        entradas.remove(sock)
                        clientes.pop(sock, None)
                        sock.close()
                        continue

                    mensaje = datos.decode("utf-8", errors="replace").strip()
                    print(f"[TCP] Recibido: '{mensaje}'")

                    # Guarda el ID_CLIENTE al procesar el primer mensaje
                    partes = mensaje.split(":")
                    if len(partes) == 3:
                        clientes[sock] = partes[0]

                    respuesta = procesar_mensaje(mensaje)
                    print(f"[TCP] Respuesta: '{respuesta}'")
                    sock.sendall((respuesta + "\n").encode())

    except KeyboardInterrupt:
        print("\n[TCP] Servidor detenido.")
    finally:
        servidor.close()


if __name__ == "__main__":
    iniciar_servidor()