from collections import OrderedDict
import sqlite3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
import platform
from dotenv import load_dotenv
import time
from threading import Thread

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')  # Required for Flask-SocketIO
socketio = SocketIO(app, async_mode='threading')  # Initialize Flask-SocketIO

# --- Database Configuration ---
DATABASE_FILE = 'sensor_data.db'  # Adjust if needed
DB_Table = 'sensor_data'  # Adjust if needed

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_data_by_interval(interval_hours):
    conn = get_db_connection()
    if interval_hours is None:
        data = conn.execute(f"SELECT DATE, TEMPERATURE FROM {DB_Table}").fetchall()
    else:
        data = conn.execute(
            f"SELECT DATE, TEMPERATURE FROM {DB_Table} WHERE date>datetime('now','localtime', '-%s hours')" % interval_hours).fetchall()
    conn.close()
    return data

@app.route('/debug')
def index():
    """ Display all records from database. Useful for debug purposes. """
    conn = get_db_connection()
    posts = conn.execute(f"SELECT * FROM {DB_Table}").fetchall()
    conn.close()
    return OrderedDict(posts)

@app.route('/temperature')
@app.route('/')
def temperature():
    data = get_data_by_interval(12)
    db_data = OrderedDict(data)
    line_dates = db_data.keys()
    line_temperatures = db_data.values()

    last_temperature = None
    if len(db_data.values()) > 1:
        last_temperature = next(reversed(db_data.values()))
    return render_template('line_chart.html', title='Temperature', labels=line_dates,
                           values=line_temperatures, last_temperature=last_temperature)

# --- Sensor Data Collection ---
get_sensor_data = None
create_table = None
save_to_db = None

def detect_platform():
    """Detects the running platform."""
    if platform.machine().startswith('arm') or os.path.exists('/proc/device-tree/soc/serial0'):
        return "pi4"
    elif os.path.exists('/sys/class/dmi/id/board_vendor') and "ASRock" in open('/sys/class/dmi/id/board_vendor').read() and \
         os.path.exists('/sys/class/dmi/id/board_name') and "X300" in open('/sys/class/dmi/id/board_name').read():
        return "x300"
    else:
        return "unknown"

platform_type = os.getenv("Platform") or detect_platform()

if platform_type == "x300":
    from Sensors.x300.sensor_loger import get_sensor_data, create_table, save_to_db
    print("Running on x300 - using x300 sensor functions.")
elif platform_type == "pi4":
    from Sensors.RPi4.pi_loger import get_sensor_data, create_table, save_to_db
    print("Running on Raspberry Pi - using RPi sensor functions.")
else:
    print(f"Unknown platform: {platform_type} - sensor data collection will not be active.")

def collect_sensor_data_periodically():
    if create_table and get_sensor_data and save_to_db:
        create_table()  # Ensure table exists
        while True:
            sensor_data = get_sensor_data() # Your sensor reading function
            if sensor_data:
                save_to_db(sensor_data) # Your database saving function
                # Emit WebSocket event with the new data
                socketio.emit('new_sensor_data', sensor_data)
            time.sleep(1)
    else:
        print("Sensor data collection is not configured for this platform.")

@app.route('/life')
def life_information():
    return render_template('life_info_ws.html') # Use a new template for WebSocket

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Connected to WebSocket server!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Start the sensor data collection in a background thread
    sensor_thread = Thread(target=collect_sensor_data_periodically, daemon=True)
    sensor_thread.start()
    socketio.run(app, host='0.0.0.0', port=9999) # Use socketio.run()