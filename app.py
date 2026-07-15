import socket
import threading
import os
from flask import Flask

app = Flask(__name__)

# Servidor TCP que fará o túnel para o tráfego da Meta
def start_tcp_server():
    # O Render atribui a porta pela variável PORT
    port = int(os.environ.get('PORT', 8080))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    
    while True:
        try:
            client, _ = server.accept()
            # Conecta ao servidor alvo (Facebook/Meta)
            target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target.connect(("www.facebook.com", 443))
            
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
            
            threading.Thread(target=pipe, args=(client, target)).start()
            threading.Thread(target=pipe, args=(target, client)).start()
        except: continue

@app.route('/')
def index():
    return "Túnel Proxy Operacional"

if __name__ == '__main__':
    # Inicia o servidor de túnel em background
    threading.Thread(target=start_tcp_server, daemon=True).start()
    # Inicia o Flask para manter o serviço ativo
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
