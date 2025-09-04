#!/usr/bin python3

import socket
import time
import os

HOST = "127.0.0.1"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando mensaje...")
    size = os.stat('../../libros/MobyDick.txt').st_size
    print(size)
    TCPClientSocket.sendall(str(size).encode())
    TCPClientSocket.recv(buffer_size)
    with open("../../libros/MobyDick.txt", "rb") as archivo:
        bloque = archivo.read( 1024)
        while(bloque!="") :
            TCPClientSocket.sendall(bloque)
            bloque = archivo.read(1024)
            if len(bloque)<1024:
                print("Último bloque b=",len(bloque))
                TCPClientSocket.sendall(b"EOT")
                break
    print("Terminé")
