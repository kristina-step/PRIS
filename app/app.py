from flask import Flask
import socket
import random
import time

app = Flask(__name__)

@app.route('/')
def hello():
    # Имитация нагрузки для CPU
    for _ in range(500000):
        _ = random.random() * random.random()
    hostname = socket.gethostname()
    return f"Hello from Pod: {hostname}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)