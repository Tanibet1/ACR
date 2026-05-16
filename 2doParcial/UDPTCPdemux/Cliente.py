"""
Cliente de prueba para ambos servidores.
Uso:
    python3 Cliente26.py tcp A1 SQR 4
    python3 Cliente26.py udp B2 NEG -7
    python3 Cliente26.py tcp C3 CUBE 3
"""

import socket
import sys

HOST = "127.0.0.1"
TCP_PORT = 65001
UDP_PORT = 65002


def enviar_tcp(cliente_id: str, operacion: str, valor: str):
    mensaje = f"{cliente_id}:{operacion}:{valor}"
    # Abre conexión, envía y espera respuesta
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, TCP_PORT))
        s.sendall((mensaje + "\n").encode())
        respuesta = s.recv(1024).decode().strip()
        print(f"[TCP] Enviado:   '{mensaje}'")
        print(f"[TCP] Respuesta: '{respuesta}'")


def enviar_udp(cliente_id: str, operacion: str, valor: str):
    mensaje = f"{cliente_id}:{operacion}:{valor}"
    # Sin conexión: envía el datagrama y espera la respuesta
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto((mensaje + "\n").encode(), (HOST, UDP_PORT))
        respuesta, _ = s.recvfrom(1024)
        print(f"[UDP] Enviado:   '{mensaje}'")
        print(f"[UDP] Respuesta: '{respuesta.decode().strip()}'")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python3 Cliente26.py <tcp|udp> <ID> <OP> <VALOR>")
        print("  Ejemplo: python3 Cliente26.py tcp A1 SQR 4")
        sys.exit(1)

    protocolo = sys.argv[1].lower()
    cid, op, val = sys.argv[2], sys.argv[3], sys.argv[4]

    if protocolo == "tcp":
        enviar_tcp(cid, op, val)
    elif protocolo == "udp":
        enviar_udp(cid, op, val)
    else:
        print("Protocolo inválido. Usa 'tcp' o 'udp'.")