import paho.mqtt.client as mqtt
import time
import random
from datetime import datetime

class MQTTModule:
    def __init__(self, device_id, broker="127.0.0.1", port=1883):
        self.device_id = device_id
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(f"{device_id}_client")
        self.status_topic = f"devices/{device_id}/status"
        self.substatus_topic = f"devices/{device_id}/substatus"
        self.counter_topic = f"devices/{device_id}/counter"
        self.last_reset_topic = f"devices/{device_id}/last_reset"
        self.software_version_topic = f"devices/{device_id}/software_version"
        self.counter = 0
        self.status = "off"
        self.substatus = None
        self.software_version = "1.0.0"  # Initialversion
        self.last_update_timestamp = None

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        print(f"{self.device_id} connected to MQTT Broker")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print(f"{self.device_id} disconnected from MQTT Broker")

    def publish(self, topic, message):
        self.client.publish(topic, message)
        print(f"Published to {topic}: {message}")

    def get_timestamp(self):
        return datetime.now().isoformat()

    def publish_status(self):
        timestamp = self.get_timestamp()
        status_message = {
            "status": self.status,
            "timestamp": timestamp
        }
        self.publish(self.status_topic, str(status_message))

        if self.status == "stop" and self.substatus:
            substatus_message = {
                "substatus": self.substatus,
                "timestamp": timestamp
            }
            self.publish(self.substatus_topic, str(substatus_message))
        else:
            substatus_message = {
                "substatus": "",
                "timestamp": ""
            }
            self.publish(self.substatus_topic, str(substatus_message))

    def publish_counter(self):
        timestamp = self.get_timestamp()
        counter_message = {
            "counter": self.counter,
            "timestamp": timestamp
        }
        self.publish(self.counter_topic, str(counter_message))

    def publish_last_reset(self):
        if self.status == "reset":
            timestamp = self.get_timestamp()
            last_reset_message = {
                "last_reset": timestamp
            }
            self.publish(self.last_reset_topic, str(last_reset_message))

    def publish_software_version(self):
        timestamp = self.get_timestamp()
        version_message = {
            "software_version": self.software_version,
            "update_timestamp": self.last_update_timestamp
        }
        self.publish(self.software_version_topic, str(version_message))

    def update_status(self, new_status, new_substatus=None):
        if new_status == "reset":
            self.status = "reset"
            self.substatus = None
            self.publish_last_reset()
        else:
            self.status = new_status
            self.substatus = new_substatus if new_status == "stop" else None
            self.publish_status()

    def update_counter(self):
        self.counter += 1
        self.publish_counter()

    def update_software_version(self, new_version):
        self.software_version = new_version
        self.last_update_timestamp = self.get_timestamp()
        self.publish_software_version()

if __name__ == "__main__":
    device1 = MQTTModule("device1")
    device2 = MQTTModule("device2")

    device1.connect()
    device2.connect()

    try:
        for _ in range(10):  # Läuft für ca. 30 Sekunden
            # Simuliere Hauptstatusänderungen und Unterstatus bei stop
            main_status = random.choice(["off", "run", "stop", "reset", "software_update"])
            substatus = random.choice(["bobin", "ayar", "cozgu", "ariza"]) if main_status == "stop" else None

            device1.update_status(main_status, substatus)
            device2.update_status(main_status, substatus)

            # Zähler aktualisieren
            device1.update_counter()
            device2.update_counter()

            # Simuliere Software-Version Updates
            if random.choice([True, False]):
                new_version = f"1.{random.randint(0, 9)}.{random.randint(0, 9)}"
                device1.update_software_version(new_version)
                device2.update_software_version(new_version)

            time.sleep(3)  # Warte 3 Sekunden
    except KeyboardInterrupt:
        print("Beendet durch Benutzer")

    device1.disconnect()
    device2.disconnect()
