import time
import subprocess
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'your_secret_key'
#socketio = SocketIO(app)

import secrets
secret_key = secrets.token_hex(32)  # Generates a 64-character hex string (32 bytes)
print(secret_key)
socketio = SocketIO(app)

def get_cpu_temp():
    """Reads CPU temperature using the 'sensors' command."""
    try:
        process = subprocess.Popen(['sensors'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=5)
        print(f"Sensors Output:\n{stdout}")
        if stdout:
            for line in stdout.splitlines():
                if "Tctl" in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        temp_str = parts[1].strip()
                        # Corrected filtering logic
                        temp_value_str = ''.join(char for char in temp_str if char.isdigit() or char.isspace() or char in '.-+')
                        temp_value_str = temp_value_str.strip()
                        try:
                            temp_value = float(temp_value_str)
                            print(f"Extracted Temperature Value: {temp_value}")
                            return temp_value
                        except ValueError:
                            print(f"Error converting temperature string to float: {temp_value_str}")
                            return None
        if stderr:
            print(f"Error running sensors: {stderr}")
        return None
    except FileNotFoundError:
        print("Error: 'sensors' command not found. Make sure it's installed.")
        return None
    except subprocess.TimeoutExpired:
        print("Error: 'sensors' command timed out.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# def get_cpu_temp():
#     """Reads CPU temperature using the 'sensors' command."""
#     try:
#         process = subprocess.Popen(['sensors'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         stdout, stderr = process.communicate(timeout=5)
#         print(f"Sensors Output:\n{stdout}")  # ADD THIS LINE
#         if stdout:
#             for line in stdout.splitlines():
#                 if "Tctl" in line:
#                     parts = line.split(':')
#                     if len(parts) > 1:
#                         temp_str = parts[1].strip()
#                         temp_value_str = ''.join(filter(str.isdigit or str.isspace or (lambda s: s in '.-+'), temp_str)).strip()
#                         try:
#                             temp_value = float(temp_value_str)
#                             print(f"Extracted Temperature Value: {temp_value}") # ADD THIS LINE
#                             return temp_value
#                         except ValueError:
#                             print(f"Error converting temperature string to float: {temp_value_str}")
#                             return None
#         if stderr:
#             print(f"Error running sensors: {stderr}")
#         return None
#     except FileNotFoundError:
#         print("Error: 'sensors' command not found. Make sure it's installed.")
#         return None
#     except subprocess.TimeoutExpired:
#         print("Error: 'sensors' command timed out.")
#         return None
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return None

def temperature_generator():
    """Continuously fetches and yields CPU temperature."""
    while True:
        temp = get_cpu_temp()
        if temp is not None:
            yield temp
        else:
            yield None # Still yield something to see if the loop is running
        time.sleep(1)  # Update every 1 second

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    for temp in temperature_generator():
        print(f"Temperature Generator yielded: {temp}") # ADD THIS LINE
        if temp is not None:
            socketio.emit('cpu_temperature', {'temperature': temp})
            print(f"Emitting cpu_temperature: {temp}") # ADD THIS LINE
        else:
            socketio.emit('cpu_temperature', {'temperature': '--'}) # Emit a placeholder if temp is None
            print(f"Emitting cpu_temperature: -- (None received)") # ADD THIS LINE

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

# import time
# import subprocess
# from flask import Flask, render_template
# from flask_socketio import SocketIO

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
# socketio = SocketIO(app)

# def get_cpu_temp():
#     """Reads CPU temperature using the 'sensors' command."""
#     try:
#         process = subprocess.Popen(['sensors'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         stdout, stderr = process.communicate(timeout=5)
#         if stdout:
#             for line in stdout.splitlines():
#                 if "Tctl" in line:
#                     parts = line.split(':')
#                     if len(parts) > 1:
#                         temp_str = parts[1].strip()
#                         # Extract the numeric value and handle potential units
#                         temp_value = float(''.join(filter(str.isdigit or str.isspace or (lambda s: s in '.-+'), temp_str)).strip())
#                         return temp_value
#         if stderr:
#             print(f"Error running sensors: {stderr}")
#         return None
#     except FileNotFoundError:
#         print("Error: 'sensors' command not found. Make sure it's installed.")
#         return None
#     except subprocess.TimeoutExpired:
#         print("Error: 'sensors' command timed out.")
#         return None
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return None

# def temperature_generator():
#     """Continuously fetches and yields CPU temperature."""
#     while True:
#         temp = get_cpu_temp()
#         if temp is not None:
#             yield temp
#         time.sleep(1)  # Update every 1 second

# @app.route('/')
# def index():
#     return render_template('index.html')

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')
#     for temp in temperature_generator():
#         socketio.emit('cpu_temperature', {'temperature': temp})

# if __name__ == '__main__':
#     socketio.run(app, debug=True, host='0.0.0.0', port=5000)