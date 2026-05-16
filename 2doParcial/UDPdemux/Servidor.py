import socket

HOST, PORT, BUF = '0.0.0.0', 5000, 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
print(f"[Servidor] Escuchando en puerto {PORT}...\n")

while True:
    datos, addr = s.recvfrom(BUF)
    mensaje = datos.decode()
    print(f"[Servidor] Mensaje de {addr[0]}:{addr[1]} -> {mensaje}")
    respuesta = f"Servidor recibio tu solicitud: '{mensaje}'"
    s.sendto(respuesta.encode(), addr)