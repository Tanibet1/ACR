import socket
import threading

def udp_client(name, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ("localhost",12345)
    sock.sendto(message.encode(), server)
    data, _ = sock.recvfrom(1024)
    print(f"[{name}] recibió:", data.decode())
    sock.close()

# Crear varios clientes concurrentes
threads = []
for i in range(5):
    t = threading.Thread(target=udp_client, args=(f"Cliente-{i+1}", f"Hola {i+1}"))
    threads.append(t)
    t.start()

for t in threads:
    t.join()