# INTEGRANTES DEL DÚO
# - Barajas Pacheco Harol Fabian
# - Flores Aguilera Jorge Alexei
import socket
import time

if __name__ == "__main__":
    host = '127.0.0.1'
    puerto = 5000

    inicio = time.time()

    for i in range(100):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, puerto))
        datos = b'\x00' * 64  # paquete de exactamente 64 bytes
        sock.sendall(datos)
        sock.close()  # cierre inmediato

    fin = time.time()
    print(f"Tiempo total Fase A (100 peticiones): {fin - inicio:.2f} segundos")