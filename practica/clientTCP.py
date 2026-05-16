import socket
import os
import struct
import time

HOST = "127.0.0.1"
PORT = 65432
FILE_PATH = "datos_prueba.txt"
BLOCK_SIZE = 1024
# Cambiar a 128 para el Escenario D
BUFFER_SIZE = 65535

file_size = os.path.getsize(FILE_PATH)
filename = os.path.basename(FILE_PATH)
filename_bytes = filename.encode('utf-8')
paquetes_enviados = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_SIZE)
    s.connect((HOST, PORT))

    s.send(struct.pack("!H", len(filename_bytes)))
    s.send(filename_bytes)

    start_time = time.time()
    with open(FILE_PATH, "rb") as f:
        while True:
            data = f.read(BLOCK_SIZE)
            if not data:
                break
            s.sendall(data)
            paquetes_enviados += 1

    s.shutdown(socket.SHUT_WR)
    exec_time = time.time() - start_time

    print("\n--- RESULTADOS TCP ---")
    print(f"Paquetes enviados: {paquetes_enviados}")
    print(f"Tiempo de ejecución: {exec_time:.4f} segundos")