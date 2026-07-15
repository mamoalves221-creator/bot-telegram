import socket
import threading
import socks  # Biblioteca PySocks
import os

def handle_client(client_socket):
    try:
        # Lê o cabeçalho inicial do SOCKS5
        client_socket.recv(4096)
        client_socket.send(b"\x05\x00") # Resposta de autenticação SOCKS5
        
        # Conecta ao destino
        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target.connect(("www.facebook.com", 443))
        
        def pipe(src, dst):
            try:
                while True:
                    data = src.recv(4096)
                    if not data: break
                    dst.send(data)
            except: pass
            
        threading.Thread(target=pipe, args=(client_socket, target)).start()
        pipe(target, client_socket)
    except: pass
    finally:
        client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", int(os.environ.get("PORT", 8080))))
server.listen(5)
while True:
    client, _ = server.accept()
    threading.Thread(target=handle_client, args=(client,)).start()
