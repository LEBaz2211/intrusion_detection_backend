import paho.mqtt.subscribe as subscribe
from flask import Flask

app = Flask(__name__)

MQTT_HOST = "eu1.cloud.thethings.network"
MQTT_PORT = 1883  # Use 8883 for TLS
MQTT_USERNAME = "intrusion-monitoring-2023@ttn"
MQTT_PASSWORD = "NNSXS.XHDJM2GWBSEOYR6IWX3BW4OBZHWA4YHOQJPP4XA.6EXBCOR7TOUQ4UYNEDNIL5T3L3S4SRDYQWCKDY6S6ABJLOGWMHXA"

message = subscribe.simple(topics=['#'], hostname=MQTT_HOST, port=MQTT_PORT,
                            auth={'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}, 
                            msg_count=1)


print(f"Topic: {message.topic}")
print(f"Payload: {message.payload}")


if __name__ == '__main__':
    app.run(debug=True)
