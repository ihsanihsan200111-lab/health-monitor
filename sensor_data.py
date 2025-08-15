import random

def get_sensor_data():
    return {
        "heart_rate": random.randint(60, 100),
        "oxygen_level": random.randint(95, 100),
        "temperature": round(random.uniform(36.0, 38.0), 1),
        "fall_detected": random.choice([True, False]),
        "gps": {
            "lat": 37.7749,
            "lon": -122.4194
        }
    }
