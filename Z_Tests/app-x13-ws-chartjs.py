from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import os
from collections import deque

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key!'
socketio = SocketIO(app, async_mode='gevent')

TEMP_FILE = '/sys/class/thermal/thermal_zone0/temp'
MAX_DATA_POINTS = 30  # Number of data points to keep in the graph
temperatures = deque(maxlen=MAX_DATA_POINTS)
timestamps = deque(maxlen=MAX_DATA_POINTS)

def get_temperature():
    """Reads the temperature from the ACPI thermal zone file."""
    try:
        with open(TEMP_FILE, 'r') as f:
            temp_millidegrees = int(f.readline().strip())
            return temp_millidegrees / 1000.0
    except FileNotFoundError:
        return "N/A"
    except ValueError:
        return "N/A"

def background_task():
    """Continuously reads the temperature and emits it via WebSocket."""
    while True:
        temperature = get_temperature()
        if isinstance(temperature, (int, float)):
            temperatures.append(temperature)
            timestamp = time.strftime('%H:%M:%S')
            timestamps.append(timestamp)
            socketio.emit('new_temperature_data', {'temperature': temperature, 'timestamp': timestamp})
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index-x13-chartjs2.html', title='Real-time Temperature Graph', max_data_points=MAX_DATA_POINTS)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('initial_data', {'temperatures': list(temperatures), 'timestamps': list(timestamps)})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.start_background_task(background_task)
    socketio.run(app, debug=True, host='0.0.0.0')