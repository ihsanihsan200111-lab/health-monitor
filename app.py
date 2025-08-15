from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

# Default (fallback) data returned until real sensor data is posted
latest_data = {
    "heart_rate": 0,
    "oxygen_level": 0,
    "temperature": 0.0,
    "fall_detected": False,
    "gps": {"lat": 11.0, "lon": 11.0, "place": "Unknown"},
    "ecg_value": 0.0,
}
# Meta info describing where values came from
# Expected values: {"source": "sensor"} or {"source": "default"}
latest_meta = {"source": "Sensor are offline now"}  # start as default

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route("/data", methods=["GET"])
def get_data():
    # Compute human-readable fall status
    fall_status = "ACTIVE" if bool(latest_data.get("fall_detected")) else "NOT ACTIVE"
    fall_origin = (latest_meta.get("source") or "default").lower()

    payload = {
        **latest_data,
        "fall_status": fall_status,   # "ACTIVE" / "NOT ACTIVE"
        "fall_origin": fall_origin,   # "sensor" / "default"
        "server_time": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(payload)

@app.route("/data", methods=["POST"])
def post_data():
    global latest_data, latest_meta
    incoming = request.get_json(silent=True) or {}

    # Accept sensor readings in the root (backward compatible)
    # Optional: a 'meta' object indicating the source (sensor/default)
    meta = incoming.pop("meta", None)
    if isinstance(meta, dict) and "source" in meta:
        latest_meta = {"source": str(meta["source"]).lower()}
    else:
        # If caller didn't say, keep previous; or assume sensor if payload looks real
        # You can force default here if you prefer
        latest_meta = latest_meta or {"source": "sensor are offline now"}

    # Merge with previous so missing fields dont erase old ones
    latest_data = {**latest_data, **incoming}

    return jsonify({"status": "received", "fall_origin": latest_meta.get("source", "Sensor are offline now")})

if __name__ == "__main__":
    print("?? Server running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
