#INTEGRANTES
#Flores Aguilera Alexei
#Barajas Pacheco Harol Fabian

import socket
import time

if __name__ == "__main__":
    puerto = 6000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', puerto))

    print(f"Servidor UDP Fase A (socket único) escuchando en puerto {puerto}")
    print("Se simulará 10ms de procesamiento por paquete → esperen pérdidas")

    recibidos = 0

    try:
        while True:
            datos, addr = sock.recvfrom(1024)
            recibidos += 1
            print(f"[{recibidos}] Recibido de {addr}: {datos.decode('utf-8')}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print(f"\n=== Fase A terminada ===")
        print(f"Paquetes recibidos y procesados: {recibidos} de 500")