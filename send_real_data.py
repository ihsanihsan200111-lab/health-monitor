import time
import requests
import random

# TODO: Replace this with actual sensor code
def get_real_sensor_data():
    ecg_value = read_ecg_sensor()  # Replace with your ECG code
    return {
        "heart_rate": read_heart_rate(),  # replace with real function
        "oxygen_level": read_spo2(),      # replace with real function
        "temperature": read_temperature(),# replace with real function
        "fall_detected": detect_fall(),   # replace with real function
        "gps": {
            "lat": read_gps_lat(),        # replace with real function
            "lon": read_gps_lon(),        # replace with real function
        },
        "ecg_value": ecg_value            # only one value at a time
    }


def read_heart_rate(): return random.randint(60, 100)
def read_spo2(): return random.randint(95, 100)
def read_temperature(): return round(random.uniform(36.0, 38.5), 1)
def detect_fall(): return random.choice([False, False, True])  # simulate rare falls
def read_gps_lat(): return 37.7749
def read_gps_lon(): return -122.4194
def read_ecg_sensor(): return round(random.uniform(-1, 1), 2)  # Replace this with actual ECG sensor reading

while True:
    try:
        data = get_real_sensor_data()
        print("Sending:", data)

        # LOCAL testing (Flask running on Pi)
        # url = "http://localhost:5000/data"

        # REMOTE Flask server (Render)
        url = "https://health-monitor-s134.onrender.com/data"

        response = requests.post(url, json=data, timeout=5)
        print("Status:", response.status_code)
    except Exception as e:
        print("Error sending data:", e)

    time.sleep(0.3)  # every 300ms for ECG
