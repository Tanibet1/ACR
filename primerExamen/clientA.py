import socket
import os
import time
import struct
import random
port = 5000
document = "hamlet.txt"
file_size = os.path.getsize(document)
filename = os.path.basename(document)
sizename = filename.encode ("utf-8")
block_size = 4096

def enviar_documento (socketCliente:socket.socket, rate:int, lag:int):
    paquetes_enviados = 0
    paquetes_perdidos = 0
    socketCliente.send(struct.pack("!H", len(sizename)))
    socketCliente.send(sizename)
    start_time = time.time()
    with open(document, "rb") as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            if lag>0:
                time.sleep (lag/1000.0)
            if random.randint(1, 100) <= rate:
                paquetes_perdidos +=1
                continue
            socketCliente.sendall(data)
            paquetes_enviados += 1

    socketCliente.shutdown(socket.SHUT_WR)
    exec_time = time.time() - start_time

    print("\n--- RESULTADOS TCP ---")
    print(f"Paquetes enviados: {paquetes_enviados}")
    print(f"Tiempo de ejecución: {exec_time:.4f} segundos")

def conectar(host:str, bufferSize:int, rate:int, lag:int):
    socketCliente = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    socketCliente.connect ((host, port))
    enviar_documento(socketCliente,rate,lag)
    socketCliente.close()

def __main__():
    host = input ("Ingrese la dirección IP del servidor: ")
    bufferSize = input ("Ingrese el tamaño de buffer: ")
    rate = int(input("Ingrese el porcentaje de pérdida(0-100): "))
    lag = int(input("Ingrese el retraso en ms: "))
    conectar(host, bufferSize, rate, lag)

if __name__ == "__main__":
    __main__()