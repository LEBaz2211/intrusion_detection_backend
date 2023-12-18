from flask import Flask, jsonify, request
import json
from DBService import DatabaseService as db_service
from MQTTService import MQTTService
from flask_socketio import SocketIO
import time
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
from multiprocessing import Process
from threading import Thread

db_service = db_service("app.db")

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")


def check_device_status():
    while True:
        devices = db_service.get_devices()
        for device in devices:
            last_event = db_service.get_latest_event_log(device['device_id'])
            print(last_event)
            if last_event:
                last_event_time = datetime.strptime(last_event['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                last_event_time = last_event_time.replace(tzinfo=timezone.utc)
                time_since_last_update = datetime.now(timezone.utc) - last_event_time
                if time_since_last_update > timedelta(minutes=10):  # or however long you want to wait
                    print(f"Device {device['device_id']} has not updated in over 10 minutes")
                    socketio.emit('DEVICE_TIMEOUT', json.dumps(device['device_id']))
                    db_service.log_event(device['device_id'], 'DEVICE_TIMEOUT', datetime.now(), json.dumps({'status': 'DEVICE_TIMEOUT'}))
                    db_service.update_device_status(device['device_id'], 'DEVICE_TIMEOUT')
        time.sleep(120)

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
    payload = json.loads(message.payload.decode('utf-8'))
    try:
        event_data = payload.get('uplink_message', {}).get('decoded_payload', {})
        device_id = payload.get('end_device_ids', {}).get('device_id', 'unknown')
        event_date = datetime.strptime(payload.get('uplink_message', {}).get('settings', {}).get('time', 'unknown'), "%Y-%m-%dT%H:%M:%S.%fZ")
        event_data = event_data_to_dict(event_data)
        print(event_data)
        device = db_service.get_device(device_id)

        statuses = ['INTRUDER_DETECTED', 'INACTIVE', 'RASPBERRY_TIMEOUT', 'ACTIVE', 'DEVICE_TIMEOUT']

        if not db_service.table_is_empty("event_log", device_id) and event_data.get('status') in statuses:
            print('here')
            if db_service.get_latest_event_log_status(device_id) == event_data.get('status'):
                socketio.emit(event_data.get('status'), json.dumps(device_id))
                db_service.log_event(device_id, event_data.get('status'), event_date, json.dumps(event_data))
                if db_service.get_device_status(device_id) != 'INTRUDER_DETECTED':
                    db_service.update_device_status(device_id, event_data.get('status'))
            elif db_service.get_latest_event_log_status(device_id) in ['INACTIVE', 'RASPBERRY_TIMEOUT'] and event_data.get('status') == 'ACTIVE':
                socketio.emit('DEVICE_OPERATIONAL', json.dumps(device_id))
                db_service.log_event(device_id, 'DEVICE_OPERATIONAL', event_date, json.dumps(event_data))
                db_service.update_device_status(device_id, 'ACTIVE')
            elif db_service.get_latest_event_log_status(device_id) == 'DEVICE_TIMEOUT' and event_data.get('status') == 'INACTIVE':
                socketio.emit('DEVICE_RECONNECTED', json.dumps(device_id))
                db_service.log_event(device_id, 'DEVICE_RECONNECTED', event_date, json.dumps(event_data))
                db_service.update_device_status(device_id, 'INACTIVE')

        elif not device:
            db_service.add_device(device_id, "unknown", "unknown", None, None, None , None)
        elif event_data.get('status') != None:
            print('here2')
            db_service.log_event(device_id, event_data.get('status'), event_date, json.dumps(event_data))
            db_service.update_device_status(device_id, event_data.get('status'))
            time.sleep(0.2)

        db_service.remove_duplicate_event_logs()
    except Exception as e:
        print("There was an error parsing the payload")
        print(e.with_traceback())
        print(payload)
        raise e


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
        success = db_service.update_device(device_id, data['name'], data['status'], data['x1'],data['y1'],data['x2'],data['y2'])
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
    number = request.args.get('number', default=10, type=int)
    start_id = request.args.get('start_id', default=None, type=int)
    try:
        log = db_service.get_range_event_logs(device_id, number, start_id)
        return jsonify({"event_logs": log}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Create threads
    status_thread = Thread(target=check_device_status)
    mqtt_thread = Thread(target=mqtt_service._run)

    # Start threads
    status_thread.start()
    mqtt_thread.start()

    # Run Flask service in the main process
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)

    # Join threads
    status_thread.join()
    mqtt_thread.join()