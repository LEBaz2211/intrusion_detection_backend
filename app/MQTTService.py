import json
import threading
import paho.mqtt.client as mqtt

class MQTTService:
    def __init__(self, host, port, username, password, on_message_callback):
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password=password)

        # Set the callback that will be called for each received message
        self.client.on_message = on_message_callback

        # Connect to the MQTT broker
        self.client.connect(host, port, 60)

    def _run(self):
        # Start the network loop
        self.client.loop_forever()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def subscribe_to_device(self, device_id):
        topic = f"v3/intrusion-monitoring-2023@ttn/devices/{device_id}/up/#"
        self.subscribe(topic)

    def stop(self):
        self.client.disconnect()