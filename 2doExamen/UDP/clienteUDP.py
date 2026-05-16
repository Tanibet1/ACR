#INTEGRANTES
#Flores Aguilera Alexei
#Barajas Pacheco Harol Fabian
import socket
import random
import time

if __name__ == "__main__":
    host = '127.0.0.1'
    puerto = 6000
    num_paquetes = 500

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    inicio = time.time()

    for i in range(1, num_paquetes + 1):
        velocidad = random.uniform(0, 100)
        mensaje = f"{i:04d}:{velocidad:.2f}".encode('utf-8')
        sock.sendto(mensaje, (host, puerto))

    fin = time.time()
    print(f"Enviados {num_paquetes} datagramas UDP en {fin - inicio:.3f} segundos (sin esperas)")