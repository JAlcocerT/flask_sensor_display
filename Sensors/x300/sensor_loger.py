import subprocess
import sqlite3
import time
from datetime import datetime

DATABASE_FILE = 'sensor_data.db'

def create_table():
    """Creates the sensor_data table in the SQLite database if it doesn't exist.
    We are pulling TCTL1 (Temperature), FAN2 (rpm) and PPT (power in Watts)
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            DATE DATETIME DEFAULT CURRENT_TIMESTAMP,
            TEMPERATURE REAL,
            fan2 INTEGER,
            ppt REAL
        )
    ''')
    conn.commit()
    conn.close()

def get_sensor_data():
    """Runs the 'sensors' command and parses the output for Tctl, fan2, and PPT."""
    sensor_data = {}
    try:
        process = subprocess.run(['sensors'], capture_output=True, text=True, check=True)
        output = process.stdout.strip().split('\n')

        for line in output:
            if "Tctl:" in line:
                parts = line.split(':')
                if len(parts) > 1:
                    value = parts[1].strip().replace('+', '').replace('°C', '')
                    try:
                        sensor_data['Tctl'] = float(value)
                    except ValueError:
                        sensor_data['Tctl'] = None
            elif "fan2:" in line:
                parts = line.split(':')
                if len(parts) > 1:
                    value_with_unit = parts[1].strip().split()[0]
                    try:
                        sensor_data['fan2'] = int(value_with_unit)
                    except ValueError:
                        sensor_data['fan2'] = None
            elif "PPT:" in line:
                parts = line.split(':')
                if len(parts) > 1:
                    value_with_unit = parts[1].strip().split()[0]
                    try:
                        sensor_data['PPT'] = float(value_with_unit)
                    except ValueError:
                        sensor_data['PPT'] = None
    except subprocess.CalledProcessError as e:
        print(f"Error running sensors command: {e}")
        return None
    except FileNotFoundError:
        print("Error: The 'sensors' command was not found.")
        return None
    return sensor_data

def save_to_db(data):
    """Saves the sensor data to the SQLite database."""
    if not data:
        return

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_data (TEMPERATURE, fan2, ppt)
        VALUES (?, ?, ?)
    ''', (data.get('Tctl'), data.get('fan2'), data.get('PPT')))
    conn.commit()
    conn.close()
    print(f"Data saved to {DATABASE_FILE} at {datetime.now()}")

if __name__ == "__main__":
    create_table()  # Ensure the table exists

    while True:
        sensor_data = get_sensor_data()
        if sensor_data:
            save_to_db(sensor_data)
        time.sleep(1)  # Collect data every 5 seconds (adjust as needed)