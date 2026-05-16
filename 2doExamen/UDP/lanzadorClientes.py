#INTEGRANTES
#Flores Aguilera Alexei
#Barajas Pacheco Harol Fabian
import subprocess
import sys
import time

if __name__ == "__main__":
    num_clientes = int(input("¿Cuántos clientes quieres lanzar? (ej: 20): "))
    script_cliente = input("Nombre del script del cliente:  ").strip()

    print(f"Lanzando {num_clientes} clientes de {script_cliente}...\n")

    procesos = []
    for i in range(num_clientes):
        p = subprocess.Popen([sys.executable, script_cliente])
        procesos.append(p)
        print(f"Cliente {i + 1} lanzado")
    print(f"\n¡Todos los {num_clientes} clientes están corriendo!")
    print("Presiona Ctrl + C en el servidor cuando quieras ver las métricas.\n")

    try:
        for p in procesos:
            p.wait()
    except KeyboardInterrupt:
        print("\nLanzador detenido.")