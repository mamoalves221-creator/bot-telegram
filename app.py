import socket, threading, os

def handle(client):
    try:
        # Lê o pedido inicial
        request = client.recv(4096).decode()
        if not request.startswith("CONNECT"):
            client.close()
            return
        
        # Extrai o host e a porta
        host = request.split(" ")[1].split(":")[0]
        port = int(request.split(" ")[1].split(":")[1])
        
        # Conecta ao destino
        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target.connect((host, port))
        client.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        
        def pipe(a, b):
            try:
                while True:
                    d = a.recv(4096)
                    if not d: break
                    b.send(d)
            except: pass
        
        threading.Thread(target=pipe, args=(client, target)).start()
        pipe(target, client)
    except: pass
    finally:
        client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", int(os.environ.get("PORT", 8080))))
server.listen(5)
while True:
    c, _ = server.accept()
    threading.Thread(target=handle, args=(c,)).start()
