from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=20, ping_interval=10)

# Armazena o último frame recebido para cada câmera
last_frames = {
    'camera': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera0():
    """Rota para acessar o vídeo."""
    return render_template('camera0.html')

@app.route('/video_frame', methods=['POST'])
def handle_video_frame():
    """Recebe frames de vídeo e os armazena."""
    camera_id = data['camera_id']
    frame = data['frame']

    # Verifica se o ID da câmera é válido
    if camera_id in last_frames:
        # Armazena o frame recebido para a câmera correspondente
        last_frames[camera_id] = frame
    
        # Emitir o frame para todos os clientes conectados, filtrando pela câmera
        socketio.emit(f'new_frame_{camera_id}', {'frame': frame})
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': 'Invalid camera_id'}), 400

@socketio.on('connect')
def handle_connect():
    print('Cliente de navegador conectado!')
    # Enviar o último frame de cada câmera para o cliente que se conectou
    for camera_id, frame in last_frames.items():
        if frame:
            emit(f'new_frame_{camera_id}', {'frame': frame})

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado.')

if __name__ == '__main__':
    # Iniciar o servidor Flask-SocketIO para escutar em todas as interfaces de rede
    socketio.run(app, host='0.0.0.0', port=5001)
