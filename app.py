from collections import OrderedDict
import sqlite3
from flask import Flask, render_template

import conf



app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(conf.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_data_by_interval(interval_hours):
    conn = get_db_connection()

    if interval_hours is None:
        data = conn.execute(f"SELECT DATE, TEMPERATURE FROM {conf.DB_Table}").fetchall()
    else:
        data = conn.execute(
            f"SELECT DATE, TEMPERATURE FROM {conf.DB_Table} WHERE date>datetime('now','localtime', '-%s hours')" % interval_hours).fetchall()

    conn.close()
    return data


@app.route('/debug')
def index():
    """ Display all records from database. Useful for debug purposes. """
    conn = get_db_connection()
    posts = conn.execute(f"SELECT * FROM {conf.DB_Table}").fetchall()
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


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9999)

from Sensors.x300.sensor_loger import get_sensor_data, create_table, save_to_db

import subprocess
import time
from threading import Thread

def collect_sensor_data_periodically():
    create_table()  # Ensure table exists
    while True:
        sensor_data = get_sensor_data() # Your sensor reading function
        if sensor_data:
            save_to_db(sensor_data) # Your database saving function
        time.sleep(1) # Collect every 5 seconds

if __name__ == '__main__':
    # Start the sensor data collection in a background thread
    sensor_thread = Thread(target=collect_sensor_data_periodically, daemon=True)
    sensor_thread.start()
    app.run(host='0.0.0.0', port=9999)