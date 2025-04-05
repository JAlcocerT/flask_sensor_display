import subprocess

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
                    sensor_data['Tctl'] = value
            elif "fan2:" in line:
                parts = line.split(':')
                if len(parts) > 1:
                    value_with_unit = parts[1].strip().split()[0]  # Get the first part (RPM)
                    sensor_data['fan2'] = value_with_unit
            elif "PPT:" in line:
                parts = line.split(':')
                if len(parts) > 1:
                    value_with_unit = parts[1].strip().split()[0]  # Get the first part (W)
                    sensor_data['PPT'] = value_with_unit
    except subprocess.CalledProcessError as e:
        print(f"Error running sensors command: {e}")
    except FileNotFoundError:
        print("Error: The 'sensors' command was not found. Make sure lm-sensors is installed.")
    return sensor_data

if __name__ == "__main__":
    data = get_sensor_data()
    if data:
        print("Sensor Data:")
        for key, value in data.items():
            print(f"{key}: {value}")