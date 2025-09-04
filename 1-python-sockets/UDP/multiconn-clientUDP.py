import socket
import threading


def udp_client(client_id, server_host, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"Hola desde cliente {client_id}"
    sock.sendto(message.encode(), (server_host, server_port))

    response, _ = sock.recvfrom(1024)
    print(f"Cliente {client_id} recibió: {response.decode()}")
    sock.close()


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
NUM_CLIENTS = 5

threads = []
for i in range(NUM_CLIENTS):
    thread = threading.Thread(target=udp_client, args=(i, SERVER_HOST, SERVER_PORT))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
