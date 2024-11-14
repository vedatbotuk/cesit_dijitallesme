import paho.mqtt.client as mqtt
import time
import random
from datetime import datetime
import threading
from .log_info import LogInfo
from .json_funcs import get_setup

class MQTTModule:
    def __init__(self, device_id, broker="127.0.0.1", port=1883):
        config_json = get_setup()

        self.logging = LogInfo(config_json['main']['log'],
                               config_json['main']['log_level'],
                               config_json['main']['log_path'])

        self.device_id = device_id
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(f"{device_id}_client")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.is_connected = False
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
        self.check_interval = 30  # Interval für die Statusüberprüfung in Sekunden
        self.check_thread = None
        self.running = False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.is_connected = True
            self.logging.log_info(f"{self.device_id} connected to MQTT Broker successfully")
        else:
            self.is_connected = False
            self.logging.log_error(f"{self.device_id} failed to connect with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        self.is_connected = False
        self.logging.log_info(f"{self.device_id} disconnected from MQTT Broker with result code {rc}")

    def on_publish(self, client, userdata, mid):
        self.logging.log_info(f"{self.device_id} message published with message id {mid}")

    def connect(self):
        try:
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
            # Give some time for connection to be established
            time.sleep(1)
            if not self.is_connected:
                self.logging.log_error("Initial connection failed. Starting connection check thread...")
                self.start_check_thread()  # Starte den Überprüfungs-Thread, auch wenn die erste Verbindung fehlschlägt
        except Exception as e:
            self.logging.log_error(f"Failed to connect: {e}")
            self.is_connected = False
            self.logging.log_error("Starting connection check thread...")
            self.start_check_thread()  # Starte den Überprüfungs-Thread, auch wenn eine Ausnahme auftritt

    def disconnect(self):
        try:
            self.running = False
            if self.check_thread and self.check_thread.is_alive():
                self.check_thread.join()  # Warte, bis der Überprüfungs-Thread beendet ist
            self.client.loop_stop()
            self.client.disconnect()
            self.logging.log_info(f"{self.device_id} disconnected from MQTT Broker")
        except Exception as e:
            self.logging.log_error(f"Failed to disconnect: {e}")

    def publish(self, topic, message):
        if not self.is_connected:
            self.logging.log_error(f"Cannot publish to {topic}: Not connected to MQTT Broker")
            return

        try:
            result = self.client.publish(topic, message)
            # result.rc == 0 means the message was sent successfully
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                self.logging.log_error(f"Failed to publish to {topic}: {result.rc}")
        except Exception as e:
            self.logging.log_error(f"Failed to publish to {topic}: {e}")

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

    def check_connection_status(self):
        while self.running:
            if not self.is_connected:
                self.logging.log_info(f"{self.device_id} is not connected. Attempting to reconnect...")
                self.connect()
            time.sleep(self.check_interval)

    def start_check_thread(self):
        if not self.check_thread or not self.check_thread.is_alive():
            self.running = True
            self.check_thread = threading.Thread(target=self.check_connection_status)
            self.check_thread.start()

# if __name__ == "__main__":
#     device1 = MQTTModule("device1")
#     device2 = MQTTModule("device2")

#     device1.connect()
#     device2.connect()

#     try:
#         for _ in range(10):  # Läuft für ca. 30 Sekunden
#             # Simuliere Hauptstatusänderungen und Unterstatus bei stop
#             main_status = random.choice(["off", "run", "stop", "reset", "software_update"])
#             substatus = random.choice(["bobin", "ayar", "cozgu", "ariza"]) if main_status == "stop" else None

#             device1.update_status(main_status, substatus)
#             device2.update_status(main_status, substatus)

#             # Zähler aktualisieren
#             device1.update_counter()
#             device2.update_counter()

#             # Simuliere Software-Version Updates
#             if random.choice([True, False]):
#                 new_version = f"1.{random.randint(0, 9)}.{random.randint(0, 9)}"
#                 device1.update_software_version(new_version)
#                 device2.update_software_version(new_version)

#             time.sleep(3)  # Warte 3 Sekunden
#     except KeyboardInterrupt:
#         device1.logging.log_info("Beendet durch Benutzer")
#         device2.logging.log_info("Beendet durch Benutzer")

#     device1.disconnect()
#     device2.disconnect()