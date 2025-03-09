from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Dictionary to store categorized sensor readings
sensor_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def store_data():
    """Receive and store sensor data with calibration categories."""
    raw_data = request.json.get('data', '')
    sensor_id = request.json.get('sensor_id', 'default_sensor')  # Identify sensor
    category_inputs = request.json.get('category_inputs', {})  # Store user-defined calibration inputs
    timestamp = datetime.utcnow().isoformat()

    try:
        hall_value = float(raw_data)  # Convert to float
    except ValueError:
        return jsonify({"message": "Invalid data format"}), 400

    # Initialize sensor storage if not exists
    if sensor_id not in sensor_data:
        sensor_data[sensor_id] = []

    # Store reading with categories
    entry = {
        "timestamp": timestamp,
        "data": hall_value,
        "category_inputs": category_inputs
    }
    sensor_data[sensor_id].append(entry)

    return jsonify({"message": "Data stored", "value": hall_value, "sensor": sensor_id})

@app.route('/get_data', methods=['GET'])
def get_data():
    """Return all stored sensor data."""
    return jsonify(sensor_data)

@app.route('/delete_data', methods=['POST'])
def delete_data():
    """Delete all stored sensor data."""
    global sensor_data
    sensor_data = {}
    return jsonify({"message": "All sensor data deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
