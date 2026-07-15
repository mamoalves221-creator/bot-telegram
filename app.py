import socket
import threading
import os
from flask import Flask

app = Flask(__name__)

# Servidor TCP em uma thread separada para o túnel
def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen(5)
    while True:
        client, _ = server.accept()
        # Aqui o túnel conecta ao destino real
        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target.connect(("www.facebook.com", 443))
        
        def pipe(src, dst):
            try:
                while True:
                    data = src.recv(4096)
                    if not data: break
                    dst.send(data)
            except: pass
        
        threading.Thread(target=pipe, args=(client, target)).start()
        threading.Thread(target=pipe, args=(target, client)).start()

@app.route('/')
def index():
    return "Túnel Proxy Operacional"

if __name__ == '__main__':
    # Inicia o túnel TCP
    threading.Thread(target=start_tcp_server).start()
    # Inicia o Flask para manter o serviço vivo no Render
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
