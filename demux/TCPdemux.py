import socket

HOST="localhost"
PORT=5050
BUFFER_SIZE=1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketServer:
    socketServer.bind((HOST, PORT))
    socketServer.listen(5)
    print(f"Servidor listo y escuchando")
    while True:
        conn, addr = socketServer.accept()
        with conn:
            print(f"Cliente conectado: {addr}")
            while True:
                print("Esperando a recibir datos...")
                data = conn.recv(BUFFER_SIZE)
                print (f"Recibien: {data}")
                if not data:
                    break
                print("Enviando respuesta a ", addr)
                conn.sendall(data)
