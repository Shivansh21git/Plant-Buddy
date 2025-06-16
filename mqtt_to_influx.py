import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from django.conf import settings


# Connect to InfluxDB
influx_client = InfluxDBClient(url=settings.INFLUX_URL, token=settings.INFLUX_TOKEN, org=settings.INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# MQTT config

QOS_LEVEL = 1
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(settings.MQTT_TOPIC,qos=QOS_LEVEL)

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
        write_api.write(bucket=settings.INFLUX_BUCKET, org=settings.ORG, record=point)
        print("Data written to InfluxDB")
    except Exception as e:
        print("Error:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(settings.MQTT_HOST, settings.MQTT_PORT, 60)
mqtt_client.loop_forever()
