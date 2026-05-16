import socket
import struct
import time

HOST = "0.0.0.0"
PORT = 54321
# Para el Escenario D y E, cambia este valor a 128. Para el resto, usa 65535
BUFFER_SIZE = 65535

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Reducir buffer a nivel sistema operativo (Para Escenario D)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
    s.bind((HOST, PORT))
    print(f"Servidor UDP esperando... (Buffer: {BUFFER_SIZE} bytes)")

    # 1. Recibir Metadata
    data, addr = s.recvfrom(65535)  # Primer paquete siempre con buffer grande
    name_len, n_total = struct.unpack("!HI", data[:6])
    filename = data[6:6 + name_len].decode('utf-8')
    print(f"Recibiendo: {filename}. Esperando {n_total} paquetes.")

    received_seqs = set()
    latencies = []

    with open(f"udp_recibido_{filename}", "wb") as f:
        while True:
            try:
                packet, addr = s.recvfrom(65535)
                # Nuevo encabezado: Seq(I), Size(H), EOF(b), Timestamp(d) = 15 bytes
                header = packet[:15]
                payload = packet[15:]
                seq_num, block_size, eof, sent_time = struct.unpack("!IHbd", header)

                # Calcular latencia
                latency_ms = (time.time() - sent_time) * 1000
                latencies.append(latency_ms)

                if block_size > 0:
                    f.seek(seq_num * 1024)
                    f.write(payload)
                    received_seqs.add(seq_num)

                if eof: break
            except BlockingIOError:
                pass

    # --- MÉTRICAS PARA EL EXAMEN ---
    paquetes_recibidos = len(received_seqs)
    paquetes_perdidos = n_total - paquetes_recibidos

    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    # Calcular Jitter (variación de la latencia)
    jitter = sum(abs(latencies[i] - latencies[i - 1]) for i in range(1, len(latencies))) / (len(latencies) - 1) if len(
        latencies) > 1 else 0

    print("\n--- RESULTADOS UDP ---")
    print(f"Paquetes esperados: {n_total}")
    print(f"Paquetes recibidos: {paquetes_recibidos}")
    print(f"Paquetes perdidos: {paquetes_perdidos}")
    print(f"Latencia promedio: {avg_latency:.2f} ms")
    print(f"Jitter: {jitter:.2f} ms")
    print(f"¿Archivo completo?: {'Sí' if paquetes_perdidos == 0 else 'No'}")