import pathlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

Sensor = os.getenv("Platform")

#Sensor = "bme280"

if Sensor =="bme280":

    DBNAME = 'temperature.db'
    DB_Table = 'temperature'
    DBDIR = pathlib.Path(__file__).parent.resolve()
    I2C_ADDRESS = 0x76
    I2C_PORT = 1
elif Sensor == "x300":
    DBNAME = 'sensor_data.db'
    DB_Table = 'sensor_data'
    DBDIR = pathlib.Path(__file__).parent.resolve()
elif Sensor == "pi4":
    DBNAME = 'pi_sensor_data.db'
    DB_Table = 'pi_sensor_data'
    DBDIR = pathlib.Path(__file__).parent.resolve()    
    

DB_PATH = pathlib.Path.joinpath(DBDIR, DBNAME)