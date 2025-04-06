from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key!'  # Change this to something secure
socketio = SocketIO(app, async_mode='gevent')  # Using gevent for asynchronous operations

TEMP_FILE = '/sys/class/thermal/thermal_zone0/temp'

def get_temperature():
    """Reads the temperature from the ACPI thermal zone file."""
    try:
        with open(TEMP_FILE, 'r') as f:
            temp_millidegrees = int(f.readline().strip())
            return temp_millidegrees / 1000.0
    except FileNotFoundError:
        return "N/A (File not found)"
    except ValueError:
        return "N/A (Invalid data)"

def background_task():
    """Continuously reads the temperature and emits it via WebSocket."""
    while True:
        temperature = get_temperature()
        socketio.emit('new_temperature', {'temperature': temperature})
        time.sleep(1)  # Update every 1 second

@app.route('/')
def index():
    return render_template('index-x13.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Optionally send the initial temperature upon connection
    temperature = get_temperature()
    emit('new_temperature', {'temperature': temperature})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.start_background_task(background_task)
    socketio.run(app, debug=True, host='0.0.0.0')