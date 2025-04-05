import subprocess
import sqlite3
import time
from datetime import datetime

DATABASE_FILE = 'pi_sensor_data.db'

def create_table():
    """Creates the pi_sensor_data table in the SQLite database if it doesn't exist.
    We are pulling TEMPERATURE from the Pi.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pi_sensor_data (
            DATE DATETIME DEFAULT CURRENT_TIMESTAMP,
            TEMPERATURE REAL
        )
    ''')
    conn.commit()
    conn.close()

def get_sensor_data():
    """Runs the 'vcgencmd measure_temp' command and parses the output for CPU temperature."""
    pi_sensor_data = {}
    try:
        process = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True, check=True)
        output = process.stdout.strip()  # Output: temp=45.6'C

        if output.startswith("temp="):
            temp_str = output[5:].replace("'C", "")
            try:
                pi_sensor_data['TEMPERATURE'] = float(temp_str)
            except ValueError:
                print(f"Error: Could not parse temperature value: {temp_str}")
                return None
        else:
            print(f"Error: Unexpected output from vcgencmd: {output}")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error running vcgencmd: {e}")
        return None
    except FileNotFoundError:
        print("Error: The 'vcgencmd' command was not found. This script is likely for a Raspberry Pi.")
        return None
    return pi_sensor_data

def save_to_db(data):
    """Saves the sensor data (CPU temperature) to the SQLite database."""
    if not data or 'TEMPERATURE' not in data:
        return

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pi_sensor_data (TEMPERATURE)
        VALUES (?)
    ''', (data['TEMPERATURE'],))
    conn.commit()
    conn.close()
    print(f"Temperature saved to {DATABASE_FILE} at {datetime.now()}")

if __name__ == "__main__":
    create_table()  # Ensure the table exists

    while True:
        pi_sensor_data = get_pi_sensor_data()
        if pi_sensor_data and 'TEMPERATURE' in pi_sensor_data:
            save_to_db(pi_sensor_data)
        time.sleep(1)  # Collect data every 1 second