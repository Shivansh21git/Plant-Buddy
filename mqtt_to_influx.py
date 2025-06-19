import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
# from django.conf import settings
from dotenv import load_dotenv
import os
load_dotenv()

INFLUX_URL = os.getenv('INFLUXDB_URL')
INFLUX_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUX_ORG = os.getenv('INFLUXDB_ORG')
INFLUX_BUCKET = os.getenv('INFLUXDB_BUCKET')

MQTT_TOPIC = os.getenv('MQTT_PUB_TOPIC')
MQTT_HOST = os.getenv('MQTT_BROKER')
MQTT_PORT  = int(os.getenv('BROKER_PORT',1883))

# Connect to InfluxDB
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# MQTT config

QOS_LEVEL = 1
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC,qos=QOS_LEVEL)

def on_message(client, userdata, msg):
    print(f"Received: {msg.payload}")
    try:
        data = json.loads(msg.payload.decode())
        point = (
            Point("npk_data")
            .tag("device_id", data["device_id"])
            .field("N", float(data["N"]))
            .field("P", float(data["P"]))
            .field("K", float(data["K"]))
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print("Data written to InfluxDB")
    except Exception as e:
        print("Error:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
