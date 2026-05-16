# INTEGRANTES DEL DÚO
# - Barajas Pacheco Harol Fabian
# - Flores Aguilera Jorge Alexei

import socket
import time

HOST = "localhost"
PORT = 5000


def ejecutar_fase_a():
    print("Iniciando Fase A: 100 Peticiones Efímeras...")
    start_time = time.time()

    for i in range(100):
        # 1. Crear nuevo socket por cada iteración
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2. Conectar
        s.connect((HOST, PORT))

        # 3. Enviar ~64 bytes
        mensaje = f"DATO_SENSOR_{i:02d}_" + ("X" * 50)
        s.sendall(mensaje.encode())

        # Esperar confirmación
        try:
            s.recv(1024)
        except Exception:
            pass

        # 4. Cerrar socket inmediatamente
        s.close()

    tiempo_total = time.time() - start_time

    print("\n--- RESULTADOS FASE A ---")
    print(f"Total de peticiones: 100")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")


if __name__ == "__main__":
    ejecutar_fase_a()