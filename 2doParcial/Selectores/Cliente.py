import socket
import time
import random
import sys

HOST = "127.0.0.1"
PORT = 65432

def simular_sensor(sensor_id: str, intervalo: float = 3.0) -> None:
    # Abre una conexión TCP con el servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[{sensor_id}] Conectado al servidor.")

        try:
            while True:
                # Genera un valor aleatorio y lo envía en formato sensor_id,valor
                valor = round(random.uniform(10.0, 100.0), 2)
                mensaje = f"{sensor_id},{valor}\n"
                s.sendall(mensaje.encode())
                print(f"[{sensor_id}] Enviado: {valor}")
                time.sleep(intervalo)  # espera antes del próximo envío

        except KeyboardInterrupt:
            print(f"\n[{sensor_id}] Sensor detenido.")


if __name__ == "__main__":
    # Toma el nombre del sensor como argumento o usa "sensor01" por defecto
    sid = sys.argv[1] if len(sys.argv) > 1 else "sensor01"
    simular_sensor(sid)