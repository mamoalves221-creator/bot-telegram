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
        # AQUI ESTÁ O SEGREDO: Ignoramos qualquer handshake e conectamos direto ao destino
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
