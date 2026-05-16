import socket
import threading
import queue

HOST = "localhost"
PORT = 5000
WORKER_POOL_SIZE = 5


def worker_task(worker_id: int, client_queue: queue.Queue):
    print(f"[Worker-{worker_id}] Inicializado y en espera de conexiones.")

    while True:
        conn, addr = client_queue.get()
        puerto_origen = addr[1]

        print(f"[Worker-{worker_id}] Atendiendo cliente desde puerto de origen: {puerto_origen}")

        try:
            while True:
                datos = conn.recv(1024)
                if not datos:
                    break
                conn.sendall(b"OK\n")

        except ConnectionResetError:
            pass
        except Exception as e:
            print(f"[Worker-{worker_id}] Error de transmisión con puerto {puerto_origen}: {e}")
        finally:
            conn.close()
            print(f"[Worker-{worker_id}] Conexión cerrada con puerto: {puerto_origen}. Retornando al pool en espera.")
            client_queue.task_done()


def iniciar_servidor():
    client_queue = queue.Queue()

    for i in range(WORKER_POOL_SIZE):
        hilo = threading.Thread(target=worker_task, args=(i, client_queue), daemon=True)
        hilo.start()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((HOST, PORT))
        servidor.listen(100)
        print(f"Servidor Proxy TCP escuchando en {HOST}:{PORT}")
        print("Presione Ctrl+C para detener la ejecución.")

        while True:
            conn, addr = servidor.accept()
            client_queue.put((conn, addr))

    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
    finally:
        servidor.close()


if __name__ == "__main__":
    iniciar_servidor()