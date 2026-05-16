import socket

HOST = "localhost"
PORT = 5000
TOTAL_MENSAJES = 500


def enviar_mensajes_efimeros():
    print(f"Iniciando transmisión de {TOTAL_MENSAJES} mensajes...")

    for i in range(TOTAL_MENSAJES):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            try:
                cliente.connect((HOST, PORT))

                mensaje = f"Mensaje de prueba {i + 1}\n".encode('utf-8')
                cliente.sendall(mensaje)

                respuesta = cliente.recv(1024)

                puerto_origen = cliente.getsockname()[1]

                print(
                    f"[{i + 1}/{TOTAL_MENSAJES}] Puerto efímero local: {puerto_origen} | Rx: {respuesta.decode().strip()}")

            except ConnectionRefusedError:
                print("\n[Excepción] Conexión rechazada. Verifique el estado del servidor.")
                break
            except Exception as e:
                print(f"\n[Excepción] Error durante la transmisión: {e}")
                break


if __name__ == "__main__":
    enviar_mensajes_efimeros()