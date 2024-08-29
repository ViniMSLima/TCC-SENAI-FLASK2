from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Armazena o último frame recebido para retransmitir para novos clientes
last_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_frame')
def handle_video_frame(data):
    global last_frame
    last_frame = data
    # Emitir o frame para todos os clientes conectados
    socketio.emit('new_frame', data)  # Remover broadcast=True

@socketio.on('connect')
def handle_connect():
    print('Cliente de navegador conectado!')
    if last_frame:
        emit('new_frame', last_frame)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
