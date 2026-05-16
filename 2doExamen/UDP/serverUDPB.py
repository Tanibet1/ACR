#INTEGRANTES
#Flores Aguilera Alexei
#Barajas Pacheco Harol Fabian

import socket
import threading
import queue
import time


def worker(q, lock, contador):
    while True:
        datos, addr = q.get()
        with lock:
            contador[0] += 1
            num = contador[0]
        print(f"[{num}] Worker procesó de {addr}: {datos.decode('utf-8')}")
        time.sleep(0.01)  # 10ms
        q.task_done()


if __name__ == "__main__":
    puerto = 6000
    num_workers = int(input("Ingrese tamaño del pool de workers (recomendado 5-10): "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', puerto))

    q = queue.Queue()
    lock = threading.Lock()
    contador = [0]


    def receptor():
        while True:
            datos, addr = sock.recvfrom(1024)
            q.put((datos, addr))


    threading.Thread(target=receptor, daemon=True).start()

    for _ in range(num_workers):
        threading.Thread(target=worker, args=(q, lock, contador), daemon=True).start()

    print(f"Servidor UDP Fase B (Worker Pool de {num_workers} hilos) escuchando en {puerto}")
    print("El receptor vacía el buffer instantáneamente → mínima pérdida")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n=== Fase B terminada ===")
        print(f"Paquetes recibidos y procesados: {contador[0]} de 500")