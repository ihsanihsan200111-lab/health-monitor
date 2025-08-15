from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

latest_data = {
    "heart_rate": 75,
    "oxygen_level": 98,
    "temperature": 36.7,
    "fall_detected": False,
    "gps": {
        "lat": 37.7749,
        "lon": -122.4194,
        "place":"Mosul"
    },
    "ecg_value":0.25
}

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(latest_data)

@app.route("/data", methods=["POST"])
def post_data():
    global latest_data
    latest_data = request.json
    return jsonify({"status": "received"})

if __name__ == "__main__":
    print("?? Server running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
