# !/usr/bin/env python3

import socket
import sys
import threading
from datetime import datetime
#se usa un diccionario para poder guardar los datos de los users que se relacionan con su objeto socket
clients={}

def recibir_datos (conn, addr):
    try:
        nickname = conn.recv(1024).decode()
        clients[conn]= nickname
        alertNewUser =f"{nickname} ha entrado al chat desde {addr}..."
        print(alertNewUser)
        broadcast(alertNewUser, conn)

        while True:
            data= conn.recv(1024)
            if not data:
                break
            time = datetime.now()
            encodeMessg = f"{nickname} [{time.strftime('%d/%m/%Y %H:%M')}]: {data.decode()}"
            print(encodeMessg)
            broadcast(encodeMessg, conn)
    except Exception as e:
        print (f"Error con {addr}: {e}")
    finally:
        if conn in clients:
            nicknameLogOut = clients[conn]
            del clients[conn]
            broadcast(f"{nicknameLogOut} ha salido del chat... Bye Bye", conn)
        conn.close()

def broadcast (mensaje, remitente_sock):
    for sock,user in clients.items():
        if sock != remitente_sock:
            try:
                sock.send(mensaje.encode('UTF-8'))
            except:
                if sock in clients:
                    del clients[sock]
                sock.close()
def start_demux_server(host, port, maxConnections):
    serveraddr = (host, int(port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind(serveraddr)
        TCPServerSocket.listen(int(maxConnections))
        print(f"Servidor de chat listo en {host}:{port}")

        while True:
            conn, addr = TCPServerSocket.accept()
            thread = threading.Thread(target=recibir_datos, args=(conn, addr))
            thread.daemon = True
            thread.start()
            print(f"[Hilos activos]: {threading.activeCount() - 1}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usa:", sys.argv[0], "<host> <puerto> <num_conexiones>")
        sys.exit(1)
    start_demux_server (sys.argv[1], sys.argv[2], sys.argv[3])