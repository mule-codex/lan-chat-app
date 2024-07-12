from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, send, emit
from datetime import datetime
import uuid
import csv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
socketio = SocketIO(app)

messages = []

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
excel_file = os.path.join(desktop_path, 'chatlogfile', 'user_logs.xlsx')
fieldnames = ['IP Address', 'Username', 'Login Time', 'Logout Time', 'Duration']

@app.route('/')
def index():
    if 'username' not in session:
        return render_template('username.html')
    return render_template('index.html', messages=messages)

@app.route('/set_username', methods=['POST'])
def set_username():
    session['username'] = request.form['username']
    session['id'] = str(uuid.uuid4())
    log_user(session['username'], request.remote_addr, datetime.now(), None)
    return render_template('index.html', messages=messages)

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

def log_user(username, ip_address, login_time, logout_time):
    os.makedirs(os.path.dirname(excel_file), exist_ok=True)   
    with open(excel_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        
        if isinstance(login_time, datetime):
            login_time_str = login_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            login_time_str = ''
        
        if isinstance(logout_time, datetime):
            logout_time_str = logout_time.strftime('%Y-%m-%d %H:%M:%S')
            duration = str(logout_time - login_time)
        elif logout_time == 'Active':
            logout_time_str = 'Active'
            duration = 'Active'
        else:
            logout_time_str = ''
            duration = ''
        
        writer.writerow({
            'IP Address': ip_address,
            'Username': username,
            'Login Time': login_time_str,
            'Logout Time': logout_time_str,
            'Duration': duration
        })

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
