import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
# InfluxDB config
bucket = "plantbuddy"
org = "myorg"
token = "ll68ar-kpu7RmwjXzlicjaHtx0N6vKFLANGHc-upvXmkIB4h7P9z9AbpljEJhlNBnr781ORNc3PoddTgAqS3EA=="
url = "http://localhost:8086"

# Connect to InfluxDB
influx_client = InfluxDBClient(url=url, token=token, org=org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# MQTT config
MQTT_BROKER = "localhost"
MQTT_TOPIC = "plantbuddy/data"
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
        write_api.write(bucket=bucket, org=org, record=point)
        print("Data written to InfluxDB")
    except Exception as e:
        print("Error:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_forever()
