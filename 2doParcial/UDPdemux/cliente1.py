import socket, time
SERVER_IP, PORT = '192.168.0.127', 5000
nombre = "Cliente 1 - Skype"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(10)
print(f"[{nombre}] Esperando 5 segundos antes de iniciar...")
time.sleep(5)
for n in range(1, 6):
    mensaje = f"Solicitud {n} desde {nombre}"
    s.sendto(mensaje.encode(), (SERVER_IP, PORT))
    print(f"[{nombre}] Enviado: {mensaje}")
    try:
        resp, _ = s.recvfrom(1024)
        print(f"[{nombre}] Respuesta: {resp.decode()}")
    except:
        print(f"[{nombre}] Sin respuesta")
    time.sleep(3)
s.close()
print(f"[{nombre}] Listo")
