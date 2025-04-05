<div align="center">
  <h1>Flask Sensor Display</h1>
</div>

<div align="center">
  <h3>Many Sensors - One Flask Web App</h3>
</div>

<div align="center">
  <h4>BME280 | x300 | Pi4 </h3>
</div>


<div align="center">
  <a href="https://github.com/JAlcocerT/Streamlit-MultiChat?tab=GPL-3.0-1-ov-file" style="margin-right: 5px;">
    <img alt="Code License" src="https://img.shields.io/badge/License-GPLv3-blue.svg" />
  </a>
  <a href="https://github.com/JAlcocerT/Streamlit-MultiChat/actions/workflows/Streamlit_GHA_MultiArch.yml" style="margin-right: 5px;">
    <img alt="GH Actions Workflow" src="https://github.com/JAlcocerT/Streamlit-MultiChat/actions/workflows/Streamlit_GHA_MultiArch.yml/badge.svg" />
  </a>

  <a href="https://www.python.org/downloads/release/python-312">
    <img alt="Python Version" src="https://img.shields.io/badge/python-3.12-blue.svg" />
  </a>
</div>

<div align="center">

[![GitHub Release](https://img.shields.io/github/release/JAlcocerT/Streamlit-MultiChat/all.svg)](https://github.com/JAlcocerT/Streamlit-MultiChat/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date-pre/JAlcocerT/Streamlit-MultiChat.svg)](https://github.com/JAlcocerT/Streamlit-MultiChat/releases)

</div>

<p align="center">

  <a href="https://youtube.com/@JAlcocerTech">
    <img alt="YouTube Channel" src="https://img.shields.io/badge/YouTube-Channel-red" />
  </a>
  <a href="https://GitHub.com/JAlcocerT/Docker/graphs/commit-activity" style="margin-right: 5px;">
    <img alt="Maintained" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" />
  </a>
  <a href="https://github.com/JAlcocerT/Docker">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/JAlcocerT/Docker" />
  </a>
  <a href="https://github.com/JAlcocerT/Docker">
    <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/JAlcocerT/Docker" />
  </a>
</p>

Tinkering with IoT and Hardware sensor information in real time with a Flask Web App


The original project reads data from a BME280 sensor.

I have adapted it to read also:

* CPU Temperature
    * for x300
    * for a Pi4
* BME280 as the original project


<details>
  <summary>Get Python and the env ready to run the Flask Web App 👈</summary>
  &nbsp;

```sh
sudo apt update
sudo apt install build-essential software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

sudo apt install python3.11 -y
```

```sh
sudo apt install python3-pip
sudo apt install python3.10-venv
#apt install python3.12-venv
#sudo apt install python3.12-dev
```


```sh
git clone https://github.com/JAlcocerT/flask_sensor_display
#git clone https://github.com/KarolPWr/flask_sensor_display.git
#git checkout tags/v1.0.0
```

```sh
#python -m venv solvingerror_venv #create the venv
python3 -m venv flaskwebapp_venv #create the venv

#solvingerror_venv\Scripts\activate #activate venv (windows)
source flaskwebapp_venv/bin/activate #(linux)
```

```sh
pip3 install -r requirements.txt
```

</details>

Tweak the `.env` file with any of the values: `bme280`, `x300` or `pi4` and just:

```sh
#python3 create_db.py
python3 app.py
```

[Alternatively, deploy as per **these instructions** →](https://github.com/JAlcocerT/flask_sensor_display/tree/main/Z_DeployMe)

Commented the process at [this post](https://jalcocert.github.io/JAlcocerT/web-apps-with-flask/)

> Forked from: https://github.com/KarolPWr/flask_sensor_display

---

# Web interface for Raspberry Pi temperature monitor

Software: Flask + Chart.js + SQLite + systemd

Hardware: Raspberry Pi + BME280

Sample chart with temperature measured in the last 12 hours:

![Alt text](chart.png?raw=true "Optional Title")

## Software setup

Clone repository to your Raspberry:

    git clone https://github.com/KarolPWr/flask_sensor_display.git

For stable version, checkout the latest tag:

    git checkout tags/v1.0.0

Install required python packages:

    pip3 install -r requirements.txt

Run install.sh script:

    bash install.sh 

Run the web server (default on localhost:9999)

    python app.py

To uninstall running project files execute:

    bash uninstall.sh

## Hardware setup 

I use Raspberry Pi Zero with Wifi and BME280 sensor. Since different versions of Raspberry are usually compatible when
it comes to GPIO and OS it should also work for other boards.

| RPi                  | BME280 |
|----------------------|--------|
| SCL (GPIO 3)         | SCL    |
| SDA (GPIO 2)         | SDA    |
| 3v3 (GPIO 1)         | VCC    |
| GND (any ground pin) | GND    |

If you have version of BME that has CSB and SDO pins, it is not necessary to connect them. However, sometimes due to
different board versions I2C addresses can get mixed up. 

Remember to enable i2c via `raspi-config`

To confirm what address your sensor has, connect it to Raspberry and run command:

    i2cscan -y <BUS>

Bus in my case was number 1, it could also be 0 or 2. Try different combinations 

## Development 

I normally develop application on desktop and deploy application to Raspberry remotely. To facilitate that, you can use helper script:

    bash deploy_to_rpi.sh -i <RASPBERRY_IP> -d <DESTINATION_PATH>

Which will copy project files to specified folder on Raspberry, kill running python app and run the webserver. 

### Using different sensor 

To use different sensor than I, you only need to re-implement sensor reading function `read_temperature()` in `sensor_getter.py` 
and test if data is correctly written do database (DATE:REAL)

*Note:* When using BMP280, I2C address will probably be 0x77

### Configuration

Constants are defined in `conf.py` file. If you want to change i.e. sensor's I2C address or database location, you change 
them in config file it will be automatically recognized by implicated files. 


