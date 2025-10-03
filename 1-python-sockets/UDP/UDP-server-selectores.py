import selectors
import socket

sel = selectors.DefaultSelector()

# Creamos un socket UDP (no orientado a conexión)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", 12345))  # servidor escuchando en puerto 9999
sock.setblocking(False)

# Función que maneja eventos de lectura
def read(sock, mask):
    data, addr = sock.recvfrom(1024)  # recibe datos UDP
    print("Recibido:", data.decode(), "de", addr)
    # responder
    sock.sendto(b"ACK: " + data, addr)

# Registramos el socket para eventos de lectura
sel.register(sock, selectors.EVENT_READ, read)

print("Servidor UDP escuchando ")
try:
    while True:
        events = sel.select(timeout=None)  # espera eventos
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
except KeyboardInterrupt:
    print("Servidor detenido")
finally:
    sel.close()
    sock.close()