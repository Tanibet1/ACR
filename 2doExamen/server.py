# INTEGRANTES DEL DÚO
# - Barajas Pacheco Harol Fabian
# - Flores Aguilera Jorge Alexei

import socket
import select
import time

HOST = "localhost"
PORT = 5000


def iniciar_servidor_fase_a():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    # Se deja una cola grande para recibir las 100 peticiones rápidas
    servidor.listen(100)
    print(f"Servidor (Fase A) escuchando en {HOST}:{PORT}")

    entradas = [servidor]

    try:
        while True:
            # En Fase A, select() vigila todos los sockets sin restricciones
            listos, _, _ = select.select(entradas, [], [])

            for sock in listos:
                if sock is servidor:
                    # Nueva conexión efímera
                    conn, addr = servidor.accept()
                    entradas.append(conn)
                else:
                    # Recepción de datos
                    try:
                        datos = sock.recv(1024)
                    except ConnectionResetError:
                        datos = None

                    if not datos:
                        # El cliente cerró la conexión (s.close())
                        entradas.remove(sock)
                        sock.close()
                    else:
                        mensaje = datos.decode("utf-8", errors="replace").strip()
                        # print(f"Procesando -> {mensaje}") # Descomentar para ver en consola

                        # Simulación de escritura en BD
                        time.sleep(0.05)

                        # Respuesta
                        try:
                            sock.sendall(b"OK\n")
                        except:
                            pass

    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.close()


if __name__ == "__main__":
    iniciar_servidor_fase_a()