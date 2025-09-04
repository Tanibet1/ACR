import socket

# Configuración del servidor
HOST = "127.0.0.1"  # Escucha en todas las interfaces
PORT = 12345  # Puerto del servidor

# Crear socket UDP no bloqueante
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
server_socket.setblocking(False)

print(f"Servidor UDP no bloqueante escuchando en {HOST}:{PORT}...")

while True:
    try:
        # Recibir datos y dirección del cliente
       # print("a");
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"Mensaje recibido de {client_address}: {message}")

        # Responder al cliente
        response = f"Servidor recibió: {message}"
        server_socket.sendto(response.encode(), client_address)
        if not data:
            break
    except BlockingIOError:
        pass  # No hay datos disponibles, continuar el bucle
    except KeyboardInterrupt:
        print("\nServidor cerrado.")
        break

server_socket.close()