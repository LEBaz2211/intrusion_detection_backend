import paho.mqtt.subscribe as subscribe
from flask import Flask
import json
import time
from app.MQTTClientWrapper import MQTTClientWrapper

app = Flask(__name__)

MQTT_HOST = "eu1.cloud.thethings.network"
MQTT_PORT = 1883  # Use 8883 for TLS
MQTT_USERNAME = "intrusion-monitoring-2023@ttn"
MQTT_PASSWORD = "NNSXS.XHDJM2GWBSEOYR6IWX3BW4OBZHWA4YHOQJPP4XA.6EXBCOR7TOUQ4UYNEDNIL5T3L3S4SRDYQWCKDY6S6ABJLOGWMHXA"

# Usage
mqtt_client = MQTTClientWrapper(MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect()
# Do other stuff...
time.sleep(3600)
# When done, disconnect
mqtt_client.disconnect()

if __name__ == '__main__':
    app.run(debug=True)
