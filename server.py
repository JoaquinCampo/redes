import sys
import socket
import re as regex
import threading as thr

def CONTROLSTREAM(sktClient, addr):
    pattern_conectar = r"CONECTAR <(\d+)>"
    pattern_interrumpir = r"INTERRUMPIR"
    pattern_continuar = r"CONTINUAR"
    pattern_desconectar = r"DESCONECTAR"
    
    comando = ''

    ipCliente = addr[0]
    puertoUDPCliente = -1
    
    conectado = False

    try:    
        while True:
            comando = sktClient.recv(1024).decode()

            match_conectar = regex.search(pattern_conectar, comando)
            match_interrumpir = regex.search(pattern_interrumpir, comando)
            match_continuar = regex.search(pattern_continuar, comando)
            match_desconectar = regex.search(pattern_desconectar, comando)
            
            if match_conectar:
                if (not conectado):
                    conectado = True
                    puertoUDPCliente = int(match_conectar.group(1))
                    
                    clientes_mutex.acquire()
                    try:
                        sktClient.sendall("OK\n".encode())
                        clientes[(ipCliente, puertoUDPCliente)] = {"activo": True}
                    except Exception as e:
                        print(f"[SERVER] Error: {e}")
                        conectado = False
                        sktClient.sendall(f"ERROR: No se pudo conectar, intente nuevamente\n".encode())
                    finally:
                        clientes_mutex.release()

            elif match_interrumpir:
                clientes_mutex.acquire()
                try:
                    sktClient.sendall("OK\n".encode())
                    if (ipCliente, puertoUDPCliente) in clientes:
                        clientes[(ipCliente, puertoUDPCliente)]["activo"] = False
                except Exception as e:
                    sktClient.sendall(f"ERROR: No se pudo interrumpir, intente nuevamente\n".encode())
                finally:
                    clientes_mutex.release()

            elif match_desconectar:
                clientes_mutex.acquire()
                try:
                    sktClient.sendall("OK\n".encode())
                    clientes.pop((ipCliente, puertoUDPCliente), None)
                    sktClient.close()
                    break
                except Exception as e:
                    sktClient.sendall(f"ERROR: No se pudo desconectar, intente nuevamente\n".encode())
                finally:
                    clientes_mutex.release()

            elif match_continuar:
                clientes_mutex.acquire()
                try:
                    sktClient.sendall("OK\n".encode())
                    if (ipCliente, puertoUDPCliente) in clientes:
                        clientes[(ipCliente, puertoUDPCliente)]["activo"] = True
                except Exception as e:
                    sktClient.sendall(f"ERROR: No se pudo continuar, intente nuevamente\n".encode())
                finally:
                    clientes_mutex.release()

            # Limpia la variable 'comando' para procesar nuevos comandos
            comando = ''
    finally:
        sktClient.close()


host = sys.argv[1]     # IP del servidor 
port = int(sys.argv[2]) # Puerto del servidor

clientes = {}  # { (ip, puertoTCP, puertoUDP): { "activo": bool } }
clientes_mutex = thr.Lock()

print(f"[SERVER] Escuchando conexiones TCP en {host}:{port}...")
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.bind((host, port))
tcpServer.listen()

udpSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServer.bind(('127.0.0.1', 65534))

def enviarDatos():
    while True:
        try:
            data, _ = udpServer.recvfrom(4096)
            clientes_mutex.acquire()
            try:
                for (ip, _, puertoUDP), cliente_data in clientes.items():
                    if cliente_data["activo"]:
                        udpSender.sendto(data, (ip, puertoUDP))
            finally:
                clientes_mutex.release()
        except ConnectionResetError:
            print("La conexión fue interrumpida.")
            continue

thr.Thread(target=enviarDatos).start()

try:
    while True:
            try:
                sktClient, addr = tcpServer.accept()
                print(f"[SERVER] Conexión establecida con {addr[0]}:{addr[1]}")
                thr.Thread(target=CONTROLSTREAM, args=(sktClient,addr,)).start()
            except Exception as e:
                print(f"[SERVER] Error al aceptar conexión: {e}")
finally:
    tcpServer.close()
    udpServer.close()
    udpSender.close()
