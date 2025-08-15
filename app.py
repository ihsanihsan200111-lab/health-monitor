from flask import Flask, request, jsonify
from flask_cors import CORS
from sensor_data import get_sensor_data

app = Flask(name)
CORS(app)

latest_data = get_sensor_data()

@app.route("/data", methods=["POST"])
def post_data():
    global latest_data
    latest_data = request.json
    return jsonify({"status": "received"})

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(latest_data)

if name == "main":
    app.run(host="0.0.0.0", port=5000)