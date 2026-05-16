#INTEGRANTES DUPLA
# - Barajas Pacheco Harol Fabian
# - Flores Aguilera Jorge Alexei
import socket
import selectors
import time

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5000

    capacidad = int(input("Ingrese la capacidad máxima de clientes simultáneos: "))

    sel = selectors.DefaultSelector()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(capacidad)
    server_socket.setblocking(False)

    sel.register(server_socket, selectors.EVENT_READ, data=None)

    print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}")
    print(f"Capacidad: {capacidad} clientes")

    try:
        while True:

            events = sel.select()

            for key, mask in events:
                if key.data is None:
                    conn, addr = server_socket.accept()
                    print(f"[SERVIDOR] Nueva conexión aceptada desde {addr}")

                    conn.setblocking(False)
                    sel.register(conn, selectors.EVENT_READ, data=addr)

                else:
                    conn = key.fileobj
                    addr = key.data

                    try:
                        data = conn.recv(1024)
                        if data:
                            print(f"[SERVIDOR] Datos recibidos de {addr} ({len(data)} bytes)")

                            time.sleep(0.05)

                    finally:
                        sel.unregister(conn)
                        conn.close()
                        print(f"[SERVIDOR] Conexión cerrada con {addr}")

    except KeyboardInterrupt:
        print("\n[SERVIDOR] Detenido por el usuario.")
    finally:
        sel.close()
        server_socket.close()