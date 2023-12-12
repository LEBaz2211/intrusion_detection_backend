from flask import Flask, jsonify, request
import json
from DBService import DatabaseService as db_service
from MQTTService import MQTTService

db_service = db_service("app.db")

app = Flask(__name__)

# Callback function to process MQTT messages
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")
    payload = json.loads(message.payload.decode('utf-8'))
    device_id = payload.get('end_device_ids', {}).get('device_id', 'unknown')
    event_data = payload.get('uplink_message', {}).get('decoded_payload', {})
    db_service.log_event(device_id, "Uplink Received", str(event_data))

# Initialize MQTT Service with the callback
mqtt_service = MQTTService("eu1.cloud.thethings.network", 1883, 
                           "intrusion-monitoring-2023@ttn", 
                           "NNSXS.XHDJM2GWBSEOYR6IWX3BW4OBZHWA4YHOQJPP4XA.6EXBCOR7TOUQ4UYNEDNIL5T3L3S4SRDYQWCKDY6S6ABJLOGWMHXA",
                           on_message)

# Subscribe to a topic
mqtt_service.subscribe('#')

@app.route('/')
def index():
    return "MQTT Flask Backend Running"

@app.route('/add_device', methods=['POST'])
def add_device():
    data = request.json
    success = db_service.add_device(data['device_id'], data['model'], data['location'], data['installation_date'])
    if success:
        mqtt_service.subscribe_to_device(data['device_id'])
        return jsonify({"message": "Device added successfully"}), 200
    else:
        return jsonify({"error": "Device already exists"}), 409

@app.route('/get_device/<device_id>', methods=['GET'])
def get_device(device_id):
    device = db_service.get_device(device_id)
    if device:
        return jsonify({"device": device}), 200
    else:
        return jsonify({"error": "Device not found"}), 404

@app.route('/get_event_log', methods=['GET'])
def get_event_log():
    log = db_service.get_event_log()
    return jsonify({"event_log": log}), 200

if __name__ == '__main__':
    app.run(debug=True)
