from flask import Flask, jsonify, request
import json
from DBService import DatabaseService as db_service
from MQTTService import MQTTService
from flask_socketio import SocketIO
import time
from flask_cors import CORS

db_service = db_service("app.db")

app = Flask(__name__)
CORS(app)

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
    db_service.remove_duplicate_event_logs()
    try:
        event_data = payload.get('uplink_message', {}).get('decoded_payload', {})
        device_id = payload.get('end_device_ids', {}).get('device_id', 'unknown')
        event_date = payload.get('uplink_message', {}).get('settings', {}).get('time', 'unknown')
        event_data = event_data_to_dict(event_data)
        print(event_data)
        device = db_service.get_device(device_id)

        if not db_service.table_is_empty("event_log", device_id):
            if event_data.get('status') == 'INTRUDER_DETECTED':
                socketio.emit('INTRUDER_DETECTED', json.dumps(event_data.device_id))
                db_service.log_event(device_id, "INTRUDER_DETECTED", event_date, json.dumps(event_data))

            elif event_data.get('status') == 'INACTIVE' and db_service.get_latest_event_log_status(device_id) == 'INACTIVE':
                socketio.emit('INACTIVE', json.dumps(event_data.device_id))
                db_service.log_event(device_id, "INACTIVE", event_date, json.dumps(event_data))

            elif event_data.get('status') == 'RASPBERRY_TIMEOUT' and db_service.get_latest_event_log_status(device_id) == 'RASPBERRY_TIMEOUT':
                socketio.emit('RASPBERRY_TIMEOUT', json.dumps(event_data.device_id))
                db_service.log_event(device_id, "RASPBERRY_TIMEOUT", event_date, json.dumps(event_data))
            
            elif not db_service.get_event_log_by_timestamp(event_date):
                db_service.log_event(device_id, event_data.get('status'), event_date, json.dumps(event_data))
                time.sleep(0.2)

            if not device:
                db_service.add_device(device_id, "unknown", "unknown", 0, 1, 2 , 4)
            # Log the event in the database with eventdata as a JSON string only if there are no events at the exact same time
        else:
            db_service.log_event(device_id, event_data.get('status'), event_date, json.dumps(event_data))
            time.sleep(0.2)
    except Exception as e:
        print("There was an error parsing the payload")


# Initialize MQTT Service with the callback
mqtt_service = MQTTService("eu1.cloud.thethings.network", 1883, 
                           "intrusion-monitoring-2023@ttn", 
                           "NNSXS.XHDJM2GWBSEOYR6IWX3BW4OBZHWA4YHOQJPP4XA.6EXBCOR7TOUQ4UYNEDNIL5T3L3S4SRDYQWCKDY6S6ABJLOGWMHXA", on_message)

# Subscribe to a topic
mqtt_service.subscribe('v3/intrusion-monitoring-2023@ttn/devices/ecam-intrusion-monitoring-2023/up')
db_service.add_device("ecam-intrusion-monitoring-2023", "unknown", "unknown", 0, 1, 2 , 4)

@app.route('/')
def index():
    return "MQTT Flask Backend Running"

@app.route('/device', methods=['POST'])
def add_device():
    data = request.json
    try:
        success = db_service.add_device(data['device_id'], data['name'], data['status'], data['x1'],data['y1'],data['x2'],data['y2'] )
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

@app.route('/device/<device_id>', methods=['GET'])
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

@app.route('/device/<device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.json
    try:
        success = db_service.update_device(device_id,data['device_id'], data['name'], data['status'], data['x1'],data['y1'],data['x2'],data['y2'])
        if success:
            return jsonify({"message": "Device updated successfully"}), 200
        else:
            return jsonify({"error": "Device not found"}), 404
    except KeyError as e:
        return jsonify({"error": f"Missing field in request data: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/device/<device_id>', methods=['DELETE'])
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
    data = request.json
    try:
        data.get('number', 10)
        data.get('start_id', None)
        log = db_service.get_event_logs(device_id)
        return jsonify({"event_log": log}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
