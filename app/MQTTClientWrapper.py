import paho.mqtt.client as mqtt
import json

class MQTTClientWrapper:
    def __init__(self, host, port, username, password):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username, password)
        self.host = host
        self.port = port

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("#")

    def on_message(self, client, userdata, msg):
        print(f"Topic: {msg.topic}")
        payload = json.loads(msg.payload.decode('utf-8'))
        print(f"Payload: {payload.get('uplink_message').get('decoded_payload')}")

    def connect(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

