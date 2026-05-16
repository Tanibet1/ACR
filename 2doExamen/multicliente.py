import socket
import time
from concurrent.futures import ThreadPoolExecutor


def cliente_individual(client_id, num_peticiones, HOST, PORT):
    for i in range(num_peticiones):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            PACKET_SIZE = 64
            data = b'SENSOR_DATA' + b'\x00' * (PACKET_SIZE - 11)
            client_socket.sendall(data)

            client_socket.close()

        except Exception as e:
            print(f"[Cliente {client_id}] Error en petición {i + 1}: {e}")


if __name__ == "__main__":
    HOST = 'localhost'  # ← Cambia solo si el servidor está en otra máquina
    PORT = 5000

    print("[CLIENTE Fase A] Configuración dinámica\n")

    # === INPUTS DEL USUARIO ===
    num_clientes = int(input("Ingrese el número de clientes simultáneos: "))
    while num_clientes <= 0:
        print("¡Debe ser al menos 1!")
        num_clientes = int(input("Ingrese el número de clientes simultáneos: "))

    num_peticiones_por_cliente = int(input("Ingrese el número de peticiones por cliente: "))
    while num_peticiones_por_cliente <= 0:
        print("¡Debe ser al menos 1!")
        num_peticiones_por_cliente = int(input("Ingrese el número de peticiones por cliente: "))

    total_peticiones = num_clientes * num_peticiones_por_cliente

    print(f"\n[CLIENTE] Iniciando {num_clientes} clientes simultáneos...")
    print(f"   • Cada cliente hará {num_peticiones_por_cliente} peticiones")
    print(f"   • Total de peticiones: {total_peticiones}")
    print("   (Cada petición = nuevo socket → connect → send 64 bytes → close)\n")

    start_time = time.time()

    # Ejecutamos los clientes en paralelo (hasta el número que pidió el usuario)
    with ThreadPoolExecutor(max_workers=num_clientes) as executor:
        for cid in range(num_clientes):
            executor.submit(cliente_individual, cid + 1, num_peticiones_por_cliente, HOST, PORT)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n[CLIENTE Fase A] ¡Completado!")
    print(f"   • Clientes simultáneos: {num_clientes}")
    print(f"   • Peticiones totales realizadas: {total_peticiones}")
    print(f"   • Tiempo total: {total_time:.4f} segundos")
    print(f"   • Tiempo promedio por petición: {total_time / total_peticiones:.4f} segundos")