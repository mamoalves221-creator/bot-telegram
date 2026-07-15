import socket
import threading
import os
from flask import Flask

app = Flask(__name__)

# Esta função encaminha os dados entre o seu telemóvel e o site de destino
def handle_connection(client_socket):
    try:
        # Tenta conectar ao destino (exemplo genérico)
        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target.connect(("www.google.com", 443))
        
        def pipe(src, dst):
            try:
                while True:
                    data = src.recv(4096)
                    if not data: break
                    dst.send(data)
            except: pass
            
        threading.Thread(target=pipe, args=(client_socket, target)).start()
        pipe(target, client_socket)
    except Exception as e:
        print(f"Erro no túnel: {e}")
    finally:
        client_socket.close()

@app.route('/')
def index():
    return "Túnel Proxy Operacional"

if __name__ == '__main__':
    # O Render atribui a porta automaticamente
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
