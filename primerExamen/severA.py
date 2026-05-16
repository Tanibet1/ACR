import socket
import os
import time
import struct

port = 5000

def connectServer (host:str, bufferSize: int):
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, bufferSize)
    try:
        socketServer.bind ((host, port))
        socketServer.listen (5)
        print (f"Servidor TCP escuchando en {host}:{port}")
        print (f"Buffer del sistema configurado a : {bufferSize} bytes")
    except Exception as e:
        print (f"Error al iniciar: {e}")
        return
    conn, addr = socketServer.accept()
    print (f"Conexión establecida con {addr}")
    with conn:
        try:
            name= conn.recv (2)
            if not name: return
            nameSize = struct.unpack("!H", name)[0]

            filename= conn.recv (nameSize).decode ("utf-8")
            output_path = f"recibido_{filename}"
            print (f"Reciviendo archivo: {filename}")
            paquetes_recibidos = 0
            start_time = time.time()

            with open (output_path, mode="wb") as file:
                while True:
                    data = conn.recv(bufferSize)
                    if not data:
                        break
                    file.write(data)
                    paquetes_recibidos+=1
            end_time = time.time()
            total_time = end_time - start_time
            print("\n--- RESULTADOS DEL SERVIDOR ---")
            print(f"Archivo guardado como: {output_path}")
            print(f"Paquetes (iteraciones recv) recibidos: {paquetes_recibidos}")
            print(f"Tiempo de recepción: {total_time:.4f} segundos")
        except Exception as e:
            print (f"Error durante la tansferencia: {e}")

def __main__():
    host = input ("Ingrese la IP del server: ")
    try:
        bufferSize = int (input ("Ingrese el tamaño del buffer: "))
        connectServer(host, bufferSize)
    except ValueError:
        print ("Por favor, inbrese un número válido para el buffer")
if __name__ == "__main__" :
    __main__()