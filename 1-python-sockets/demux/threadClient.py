import socket
import threading
import sys

#los datos de entrada que siempre van a estar cambiando serán los de: direccion y el puerto del servidor, por lo tanto
#podemos ponerlo como un dato que el usuario tenga que ingresar
#en esta caso también vamos a pedirle su identificador para el chat

#primero lo que ya sabemos hacer, crear el socket
def connection (directionIP: str="localhost", port: int=5000, nickname:str ="user"):
    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socketClient.connect((directionIP, port))
        print(f"Conectado al servidor de chat en {directionIP}:{port}")
        socketClient.send(nickname.encode())
        thread_recv = threading.Thread (target=get_msgs, args=(socketClient,))
        thread_recv.daemon=True
        thread_recv.start()

        send_msgs(socketClient, nickname)
    except Exception as e:
        print(f"Error al conectarse al chat: {e}")


def get_msgs (socketClient):
    while True:
        try:
            message = socketClient.recv(1024).decode()
            if not message:
                print ("\n[SERVIDOR] Conexión cerrada por el server de chat")
                break
            print(f"\r{message}\nTú: ", end="", flush=True)
        except:
            print ("ERROR. Conexión perdida con el chat")
            break
    socketClient.close()
def send_msgs (socketClient, nickname):
    print (f"Bienvenido al chat {nickname}")
    print (f"Si quieres salir del chat, envía 'Salir'")
    try:
        while True:
            msgToSend = input ("Tú: ")
            if msgToSend.lower() == "salir":
                break
            if msgToSend.strip():
                socketClient.send(msgToSend.encode())
    except EOFError:
        pass
    finally:
        socketClient.close()
        print ("Conexión finalizada")

def __main__():
    nickname = input ("Ingrese su nombre: ")
    directionIP= input ("Ingrese la direccion IP del server: ")
    port= int(input ("Ingrese el puerto del server: "))
    connection(directionIP, port, nickname)

if __name__ == "__main__":
    __main__()