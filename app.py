from flask import Flask, session, request
from flask_socketio import SocketIO, send, emit
from datetime import datetime
from user import user_bp
from user_log import user_log_bp, log_user  # Import the Blueprint and function

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
socketio = SocketIO(app)

messages = []

# Register the Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(user_log_bp)

@socketio.on('message')
def handle_message(data):
    msg = {
        'id': session['id'],
        'username': session['username'],
        'text': data,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    messages.append(msg)
    send(msg, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print(f"Client connected with IP: {request.remote_addr}")
    log_user(session.get('username', 'Unknown'), request.remote_addr, datetime.now(), None)
    emit('previous_messages', messages)

@socketio.on('disconnect')
def handle_disconnect():
    logout_time = datetime.now()
    log_user(session.get('username', 'Unknown'), request.remote_addr, None, logout_time)
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
