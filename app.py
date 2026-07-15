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
    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta diretamente ao destino (Facebook)
    target.connect(("www.facebook.com", 443))
    threading.Thread(target=pipe, args=(client, target)).start()
    pipe(target, client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", int(os.environ.get("PORT", 8080))))
server.listen(5)

while True:
    client, _ = server.accept()
    threading.Thread(target=handle, args=(client,)).start()
