import socket
import struct
import time

HOST = "0.0.0.0"
PORT = 65432
# Cambiar a 128 para el Escenario D
BUFFER_SIZE = 65535

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Servidor TCP esperando... (Buffer: {BUFFER_SIZE})")

    conn, addr = s.accept()
    with conn:
        start_time = time.time()
        name_len_data = conn.recv(2)
        name_len = struct.unpack("!H", name_len_data)[0]
        filename = conn.recv(name_len).decode('utf-8')

        paquetes_recibidos = 0
        with open(f"tcp_recibido_{filename}", "wb") as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
                paquetes_recibidos += 1

        exec_time = time.time() - start_time
        print("\n--- RESULTADOS TCP ---")
        print(f"Iteraciones de lectura (Paquetes): {paquetes_recibidos}")
        print(f"Tiempo de ejecución: {exec_time:.4f} segundos")
        print(f"¿Archivo completo?: Sí (Garantizado por TCP)")