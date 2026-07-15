import socket, threading, os

def handle(client):
    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target.connect(("www.facebook.com", 443))
    def pipe(a, b):
        try:
            while True:
                d = a.recv(4096)
                if not d: break
                b.send(d)
        except: pass
    threading.Thread(target=pipe, args=(client, target)).start()
    pipe(target, client)
    client.close()
    target.close()

def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", int(os.environ.get("PORT", 8080))))
    server.listen(5)
    while True:
        c, _ = server.accept()
        threading.Thread(target=handle, args=(c,)).start()

if __name__ == "__main__":
    run()
