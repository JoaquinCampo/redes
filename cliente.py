import sys
import socket
import threading

def recibirDatos(sktUDP, sktVLC):
    while True:
        try:
            data, _ = sktUDP.recvfrom(4096)
            # Enviar al VLC
            sktVLC.sendto(data, ('127.0.0.1', vlcPort))
        except ConnectionResetError:
            pass

def CONTROLSTREAM():
    conectado = False
    while True:
        command = input("Introduce un comando (CONECTAR, INTERRUMPIR, CONTINUAR, DESCONECTAR): ").strip().upper()
        
        if command == "CONECTAR":
            if(not conectado):
                conectado = True
                command = command + " <" + str(chosen_port) + ">\n"
                sktTCP.sendall(command.encode())
                print("Conectando...")

                # Esperamos la respuesta del servidor
                data = sktTCP.recv(1024)
                print("[SERVER] " + data.decode())
            
        elif command == "INTERRUMPIR":
            sktTCP.sendall(command.encode())
            print("Interrumpiendo...")
            # Esperamos la respuesta del servidor
            data = sktTCP.recv(1024).decode()
            print("[SERVER] " + data)
            
        elif command == "CONTINUAR":
            sktTCP.sendall(command.encode())
            print("Continuando...")
            
            # Esperamos la respuesta del servidor
            data = sktTCP.recv(1024)
            print("[SERVER] " + data.decode())
            
        elif command == "DESCONECTAR":
            sktTCP.sendall(command.encode())
            print("Desconectando...")

            # Esperamos la respuesta del servidor
            data = sktTCP.recv(1024)
            print("[SERVER] " + data.decode())
            break
        
        else:
            print("Comando no reconocido. Por favor, introduzca un comando válido.")
    print("Conexión cerrada.")

# Recibimos los parametros
host = sys.argv[1] #server ip
port = int(sys.argv[2])           #server port
vlcPort = int(sys.argv[3])

# Creamos el socket TCP para conectarnos con el servidor
sktTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sktTCP.connect((host, port))    
print(f"[CLIENT] Conectado al servidor {host}:{port}")

# Creamos un socket UDP para recibir los datagramas del servidor
sktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sktUDP.bind(('0.0.0.0', 0))

# Creamos un socket UDP para redirigir los datagramas al reproductor VLC
sktVLC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Creamos un hilo para recibir los datagramas
host, chosen_port = sktUDP.getsockname()
client_thread = threading.Thread(target=recibirDatos, args=(sktUDP, sktVLC,))
client_thread.start()


if __name__ == "__main__":
    CONTROLSTREAM()