import time
import requests
from sensor_data import get_sensor_data

while True:
    try:
        data = get_sensor_data()
        print("Sending:", data)
        requests.post("http://localhost:5000/data", json=data)
    except Exception as e:
        print("Error:", e)

    time.sleep(5)
