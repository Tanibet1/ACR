import socket
import os
import struct
import time

HOST = "127.0.0.1"  # Cambia por la IP de tu VM si es necesario
PORT = 54321
FILE_PATH = "datos_prueba.txt"  # Crea un archivo de ~1MB
CHUNK_SIZE = 1024
# Para el Escenario D, cambia esto a 128
BUFFER_SIZE = 65535

filename = os.path.basename(FILE_PATH)
file_size = os.path.getsize(FILE_PATH)
total_packets = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE > 0 else 0)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_SIZE)

    # Metadata
    filename_bytes = filename.encode('utf-8')
    metadata = struct.pack("!HI", len(filename_bytes), total_packets) + filename_bytes
    s.sendto(metadata, (HOST, PORT))

    print(f"Enviando {total_packets} paquetes...")
    start_time = time.time()

    with open(FILE_PATH, "rb") as f:
        seq_num = 0
        while True:
            data = f.read(CHUNK_SIZE)
            eof = 1 if not data else 0
            # Incluimos el timestamp actual en el paquete
            header = struct.pack("!IHbd", seq_num, len(data), eof, time.time())
            s.sendto(header + data, (HOST, PORT))

            if eof: break
            seq_num += 1

    exec_time = time.time() - start_time
    print(f"--- TRANSFERENCIA FINALIZADA ---")
    print(f"Tiempo de ejecución: {exec_time:.4f} segundos")