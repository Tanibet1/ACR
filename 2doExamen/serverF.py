# INTEGRANTES DEL DÚO
# - Barajas Pacheco Harol Fabian
# - Flores Aguilera Jorge Alexei
import socket
import threading
import time


def manejar_cliente(conn, addr):
    try:
        datos = conn.recv(1024)  # recibe el paquete de 64 bytes
        time.sleep(0.05)  # simula escritura en base de datos (50 ms)
    finally:
        conn.close()  # cierre físico


if __name__ == "__main__":
    puerto = 5000
    capacidad = int(input("Ingrese la capacidad máxima de clientes simultáneos: "))

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', puerto))
    servidor.listen(100)  # backlog generoso para no rechazar conexiones

    print(f"Servidor escuchando en puerto {puerto} - Capacidad: {capacidad} clientes simultáneos")

    semaforo = threading.Semaphore(capacidad)  # limita concurrencia

    while True:
        conn, addr = servidor.accept()
        print(f"Conexión aceptada desde {addr}")


        def worker(c, a):
            with semaforo:
                manejar_cliente(c, a)


        threading.Thread(target=worker, args=(conn, addr), daemon=True).start()