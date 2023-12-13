from flask import Flask, jsonify, request
import json
from DBService import DatabaseService as db_service
from MQTTService import MQTTService
from flask_socketio import SocketIO
import time

db_service = db_service("app.db")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def event_data_to_dict(event_data):
    """Takes a string like: {"text":"device_id:1, voltage:N/A, status:active"} and converts it to a dictionary"""
    event_data = str(event_data)
    event_data = event_data.replace("\'", "").replace("{", "").replace("}", "").replace("\"", "")
    event_data = event_data.split(",")
    event_data = [item.replace(" ", "").split(":") for item in event_data]
    event_data = {item[0]: item[1] for item in event_data if item[0] != "text"}
    return event_data

# Callback function to process MQTT messages
def on_message(client, userdata, message):
    # print current thread id
    # print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")
    payload = json.loads(message.payload.decode('utf-8'))
    try:
        print(payload)
        event_data = payload.get('uplink_message', {}).get('decoded_payload', {})
        device_id = payload.get('end_device_ids', {}).get('device_id', 'unknown')
        event_date = payload.get('uplink_message', {}).get('settings', {}).get('time', 'unknown')
        event_data = event_data_to_dict(event_data)
        print(event_data)
        # Find if device exists in database and add it if it doesn't exist
        device = db_service.get_device(device_id)
        print(event_data['status'])
        if event_data.get('status') == 'intrusion':
            socketio.emit('intrusion', json.dumps(event_data), broadcast=True)
            db_service.log_event(device_id, "intrusion", event_date, json.dumps(event_data))
        if not device:
            db_service.add_device(device_id, "unknown", "unknown", "unknown")
        # Log the event in the database with eventdata as a JSON string only if there are no events at the exact same time
        if not db_service.get_event_log_by_timestamp(event_date):
            db_service.log_event(device_id, "status", event_date, json.dumps(event_data))
            time.sleep(0.2)
    except:
        print("There was an error parsing the payload")


# Initialize MQTT Service with the callback
mqtt_service = MQTTService("eu1.cloud.thethings.network", 1883, 
                           "intrusion-monitoring-2023@ttn", 
                           "NNSXS.XHDJM2GWBSEOYR6IWX3BW4OBZHWA4YHOQJPP4XA.6EXBCOR7TOUQ4UYNEDNIL5T3L3S4SRDYQWCKDY6S6ABJLOGWMHXA", on_message)

# Subscribe to a topic
mqtt_service.subscribe('v3/intrusion-monitoring-2023@ttn/devices/ecam-intrusion-monitoring-2023/up')

@app.route('/')
def index():
    return "MQTT Flask Backend Running"

@app.route('/devices', methods=['POST'])
def add_device():
    data = request.json
    try:
        success = db_service.add_device(data['device_id'], data['model'], data['location'], data['installation_date'])
        if success:
            # Subscribe to the device's MQTT topic if needed
            # mqtt_service.subscribe_to_device(data['device_id'])
            return jsonify({"message": "Device added successfully"}), 201
        else:
            return jsonify({"error": "Device already exists"}), 409
    except KeyError as e:
        return jsonify({"error": f"Missing field in request data: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    try:
        device = db_service.get_device(device_id)
        if device:
            return jsonify({"device": device}), 200
        else:
            return jsonify({"error": "Device not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/devices', methods=['GET'])
def get_devices():
    try:
        devices = db_service.get_devices()
        return jsonify({"devices": devices}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.json
    try:
        success = db_service.update_device(device_id, data.get('model'), data.get('location'), data.get('installation_date'))
        if success:
            return jsonify({"message": "Device updated successfully"}), 200
        else:
            return jsonify({"error": "Device not found"}), 404
    except KeyError as e:
        return jsonify({"error": f"Missing field in request data: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    try:
        success = db_service.delete_device(device_id)
        if success:
            return jsonify({"message": "Device deleted successfully"}), 200
        else:
            return jsonify({"error": "Device not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/event_logs/<device_id>', methods=['GET'])
def get_event_logs(device_id):
    try:
        log = db_service.get_event_logs(device_id)
        return jsonify({"event_log": log}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
