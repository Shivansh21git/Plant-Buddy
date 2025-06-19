import threading
import time
import random
import json
import paho.mqtt.client as mqtt
# from django.conf import settings
from dotenv import load_dotenv
import os
load_dotenv()


QOS_LEVEL = 1  # Change this to 0, 1, or 2

MQTT_HOST = os.getenv('MQTT_BROKER')
MQTT_TOPIC = os.getenv('MQTT_PUB_TOPIC')
MQTT_PORT  = int(os.getenv('BROKER_PORT',1883))
# print(MQTT_HOST)
# print(MQTT_TOPIC)
# print(MQTT_PORT)
# print(type(MQTT_PORT))
# Simulate a single device
def simulate_device(device_id):
    client = mqtt.Client()
    client.connect(MQTT_HOST,1883, 60)
    client.loop_start()  # Allow background processing

    while True:
        N = round(random.uniform(30.0, 70.0), 2)
        P = round(random.uniform(30.0, 70.0), 2)
        K = round(random.uniform(30.0, 70.0), 2)
        payload = json.dumps({
            "device_id": device_id,
            "N": N,
            "P": P,
            "K": K
        })
        result = client.publish(MQTT_TOPIC, payload, qos=QOS_LEVEL)
        status = result[0]
        if status == 0:
            print(f"[{device_id}] Sent (QoS {QOS_LEVEL}): {payload}")
        else:
            print(f"[{device_id}] Failed to send message")
        time.sleep(random.randint(2, 5))

# Start multiple simulated devices
device_ids = ["plant-002"]
threads = []

for device_id in device_ids:
    t = threading.Thread(target=simulate_device, args=(device_id,))
    t.daemon = True
    t.start()
    threads.append(t)


# Keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulation stopped.")
