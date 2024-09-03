from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=20, ping_interval=10)

# Armazena o último frame recebido para cada câmera
last_frames = {
    'camera_0': None,
    'camera_1': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera0')
def camera0():
    """Rota para acessar o vídeo da câmera 0."""
    return render_template('camera0.html')

@app.route('/camera1')
def camera1():
    """Rota para acessar o vídeo da câmera 1."""
    return render_template('camera1.html')

@socketio.on('video_frame')
def handle_video_frame(data):
    """Recebe frames de vídeo e os armazena."""
    global last_frames
    camera_id = data['camera_id']
    frame = data['frame']

    # Verifica se o ID da câmera é válido
    if camera_id in last_frames:
        # Armazena o frame recebido para a câmera correspondente
        last_frames[camera_id] = frame
    
        # Emitir o frame para todos os clientes conectados, filtrando pela câmera
        socketio.emit(f'new_frame_{camera_id}', {'frame': frame})

@socketio.on('connect')
def handle_connect():
    print('Cliente de navegador conectado!')
    # Enviar o último frame de cada câmera para o cliente que se conectou
    for camera_id, frame in last_frames.items():
        if frame:
            emit(f'new_frame_{camera_id}', {'frame': frame})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
