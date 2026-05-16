import socket

HOST="localhost"
PORT = 5050
BUFSIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketCliente:
    socketCliente.connect(("0.0.0.0", PORT))
    socketCliente.send(b"Oye te estoy hablando server!\n Hazme caso")
    socketCliente.recv(BUFSIZE)