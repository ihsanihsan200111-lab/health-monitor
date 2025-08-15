import time
import requests
import random
import math

API_URL = "https://health-monitor-s134.onrender.com/data"  # <-- your backend /data

# ===== Real sensor hooks (replace with your drivers) =====
def read_heart_rate(): return random.randint(60, 100)
def read_spo2(): return random.randint(95, 100)
def read_temperature(): return round(random.uniform(36.0, 38.5), 1)
def detect_fall(): return random.choice([False, False, True])  # simulate rare falls
def read_gps_lat(): return 33.3128   # <-- example: Baghdad lat; replace with real GPS
def read_gps_lon(): return 44.3615   # <-- example: Baghdad lon; replace with real GPS
def read_ecg_sensor(): return round(random.uniform(-1, 1), 2)

# ===== Reverse geocoding helpers =====
_last_lat = None
_last_lon = None
_last_place = "Detecting..."
_last_lookup_ts = 0

def haversine_m(lat1, lon1, lat2, lon2):
    """Distance in meters between two lat/lon points."""
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2)**2
    return 2 * R * math.asin(math.sqrt(a))
def reverse_geocode(lat, lon):
    """Call Nominatim to get a human-readable place for lat/lon."""
    try:
        # Respect Nominatim usage policy: set a descriptive User-Agent
        headers = {"User-Agent": "raspberry-health-dashboard/1.0 (contact: you@example.com)"}
        params = {
            "format": "json",
            "lat": str(lat),
            "lon": str(lon),
            "zoom": "14",
            "addressdetails": "1"
        }
        
        resp = requests.get("https://nominatim.openstreetmap.org/reverse",
                            headers=headers, params=params, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("display_name") or "Unknown place"
        return f"Reverse geocode failed ({resp.status_code})"
    except Exception:
        return "Place lookup error"

def get_place_name(lat, lon, now_ts):
    """
    Return a cached place name unless:
      - we moved = ~50m, or
      - 
    Also rate-limit lookups to at most once per second.
    """
    global _last_lat, _last_lon, _last_place, _last_lookup_ts

    if _last_lat is None or _last_lon is None:
        # First time: do a lookup (sleep 1s to respect Nominatim)
        time.sleep(1.05)
        _last_place = reverse_geocode(lat, lon)
        _last_lat, _last_lon = lat, lon
        _last_lookup_ts = now_ts
        return _last_place

    dist = haversine_m(lat, lon, _last_lat, _last_lon)
    time_since = now_ts - _last_lookup_ts

    if dist >= 50 or time_since >= 120:  # moved enough or stale cache
        # obey 1 req/sec
        elapsed = time.time() - _last_lookup_ts
        if elapsed < 1.05:
            time.sleep(1.05 - elapsed)
        _last_place = reverse_geocode(lat, lon)
        _last_lat, _last_lon = lat, lon
        _last_lookup_ts = now_ts

    return _last_place

# ===== Compose your payload =====
def get_real_sensor_data():
    lat = read_gps_lat()
    lon = read_gps_lon()
    now_ts = time.time()
    place = get_place_name(lat, lon, now_ts)

    return {
        "heart_rate": read_heart_rate(),
        "oxygen_level": read_spo2(),
        "temperature": read_temperature(),
        "fall_detected": detect_fall(),
        "gps": {
            "lat": lat,
            "lon": lon,
            "place": place,          # <-- human-readable place added
        },
        "ecg_value": read_ecg_sensor()
    }

# ===== Main loop =====
session = requests.Session()  # reuse TCP connection
while True:
    try:
        data = get_real_sensor_data()
        print("Sending:", data)
        resp = session.post(API_URL, json=data, timeout=5)
        print("Status:", resp.status_code)
    except Exception as e:
        print("Error sending data:", e)

    # ECG cadence: ~300 ms; adjust if your CPU/network is busy
    time.sleep(0.3)
