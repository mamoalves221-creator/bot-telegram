import os
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/<path:url>')
def proxy(url):
    target_url = request.url.replace(request.host_url, 'https://')
    resp = requests.get(target_url)
    return resp.content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
