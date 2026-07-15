import socket, threading, os

def pipe(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data: break
            dst.send(data)
    except: pass
    finally:
        src.close()
        dst.close()

def handle(client):
    try:
        # SOCKS5 Handshake simples
        client.recv(4096)
        client.send(b"\x05\x00") # Resposta: Versão 5, Sem autenticação
        
        # Lê o pedido de conexão
        data = client.recv(4096)
        # Resposta: SOCKS5 sucesso
        client.send(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
        
        # Conecta ao destino
        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target.connect(("www.facebook.com", 443))
        
        threading.Thread(target=pipe, args=(client, target)).start()
        pipe(target, client)
    except: client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", int(os.environ.get("PORT", 8080))))
server.listen(5)

while True:
    client, _ = server.accept()
    threading.Thread(target=handle, args=(client,)).start()
