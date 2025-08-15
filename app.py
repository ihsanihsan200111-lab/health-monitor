from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sensor_data import get_sensor_data
import os

app = Flask(__name__, static_folder='static')
CORS(app)

latest_data = get_sensor_data()

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

if __name__ == "main":
    app.run(host="0.0.0.0", port=5000)
