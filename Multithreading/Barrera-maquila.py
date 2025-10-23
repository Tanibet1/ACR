import threading
import time
import random

N = 4
barrera = threading.Barrier(N)

def trabajador(id):
    # Fase 1: Ensamblaje
    print(f"Trabajador {id} ensamblando piezas...")
    time.sleep(random.uniform(0.5, 2.0))
    print(f"Trabajador {id} terminó la fase de ensamblaje.")
    barrera.wait()

    # Fase 2: Revisión de calidad
    print(f" Trabajador {id} revisando calidad...")
    if id == 2:
        time.sleep(1.5)  # da tiempo a que los demás lleguen a la barrera
        print(f"Trabajador {id} tuvo un problema y abandonó la línea.")
        return  # rompe la sincronización
    time.sleep(random.uniform(0.5, 2.0))
    print(f" Trabajador {id} terminó la revisión de calidad.")
    barrera.wait()

    # Fase 3: Empaque final
    print(f"Trabajador {id} empaquetando productos...")
    time.sleep(random.uniform(0.5, 2.0))
    print(f" Trabajador {id} completó todo el lote.")

# Crear hilos
hilos = [threading.Thread(target=trabajador, args=(i+1,)) for i in range(N)]

for h in hilos:
    h.start()

for h in hilos:
    h.join()

print("\nFin del turno de producción.")
