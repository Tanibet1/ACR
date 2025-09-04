#!/usr/bin python3
import socket
HOST = "localhost"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432 # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as  ServerAccept:
    ServerAccept.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ServerAccept.bind((HOST, PORT))
    ServerAccept.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")

    socket_conn, Client_addr = ServerAccept.accept()
    with socket_conn:
        print("Conectado a", Client_addr)
        while True:
            print("Esperando a recibir datos... ")
            data = socket.recv(buffer_size)
            print ("Recibido,", data,"   de ", Client_addr)
            print (len(data))
            if not data:
                break
        print("Terminé")

