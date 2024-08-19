""" Use paho-mqtt<2.0.0 """

import paho.mqtt.client as mqtt

class MQTTModule:
    def __init__(self, broker, port, topic, client_id="mqtt_client"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.client.subscribe(self.topic)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

    def publish(self, message):
        self.client.publish(self.topic, message)
        print(f"Published message: {message} to topic: {self.topic}")

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT Broker")

"""
if __name__ == "__main__":
    broker = "test.mosquitto.org"
    port = 1883
    topic = "test/topic"

    mqtt_module = MQTTModule(broker, port, topic)
    mqtt_module.connect()

    # Test: Nachricht senden und empfangen
    mqtt_module.publish("Hello MQTT!")

    # Warte für eingehende Nachrichten (z.B. 10 Sekunden)
    import time
    time.sleep(10)

    mqtt_module.disconnect()
"""