import socket

HOST = "127.0.0.1"  # El hostname o IP del servidor
PORT = 54321  # El puerto usado por el servidor
msgFromClient = "Hola servidor UDP "
bytesToSend = str.encode(msgFromClient)
serverAddressPort = (HOST, PORT)
bufferSize = 1024

# Crea un socket UDP del lado del cliente

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
    # Enviando mensaje al servidor usando el socket UDP
    cont = 0
    for i in range(1, 101):
        mensaje = f"El cliente UDP con la IP {HOST} y el puerto {PORT} mandó el mensaje número {i} "
        bytesToSend = str.encode(mensaje)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        print("Mensaje del servidor {}".format(msgFromServer[0]))
        UDPClientSocket.sendto(b'', serverAddressPort)




    