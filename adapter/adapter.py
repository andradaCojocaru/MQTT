"""
MQTT subscriber - Listen to a topic and sends data to InfluxDB
"""

from datetime import datetime
import json
import sys
import os
import re
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS
import paho.mqtt.client as mqtt

load_dotenv()  # take environment variables from .env.

def is_valid_topic(topic):
    pattern = re.compile(r'^\w+/[^\s/]+$')
    return bool(pattern.match(topic))

def is_valid_json(message):
    try:
        json_object = json.loads(message)
        return isinstance(json_object, dict)
    except json.JSONDecodeError:
        return False
    
def extract_location_and_station(topic):
    parts = topic.split("/")
    location = parts[0]
    station = parts[1]
    return location, station

# InfluxDB config
BUCKET = os.getenv('INFLUXDB_BUCKET')
client = InfluxDBClient(url=os.getenv('INFLUXDB_URL'),
                token=os.getenv('INFLUXDB_TOKEN'), org=os.getenv('INFLUXDB_ORG'))
write_api = client.write_api()

# MQTT broker config
MQTT_BROKER_URL    = "mqtt.eclipseprojects.io"
MQTT_PUBLISH_TOPIC = "#"

mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER_URL)

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client connects to the broker."""
    print("Connected with result code "+str(rc))

    # Subscribe to a topic
    client.subscribe(MQTT_PUBLISH_TOPIC)

def on_message(client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the server."""
    if is_valid_topic(msg.topic):
        if is_valid_json(msg.payload):
            print(f"Received a message by topic: [{msg.topic}]")

            try:
                data = json.loads(msg.payload.decode("utf-8"))

                # Extract relevant fields
                timestamp = data.get("timestamp")
                if timestamp is None:
                    timestamp = datetime.now().isoformat()
                    print(f"Data timestamp is NOW")
                else:
                    print(f"Data timestamp is: {timestamp}")
                location, station = extract_location_and_station(msg.topic)

                # add only numerical fields
                for key, value in data.items():
                    if isinstance(value, (int, float)):
                        point = Point(f'{station}.{key}').tag("location", location).tag("station", station)
                        point.field(key, value)
                        if isinstance(timestamp, str):
                            timestamp_datetime = datetime.fromisoformat(timestamp)
                            point.time(timestamp_datetime, WritePrecision.S)
                            print(f"{location}.{station}.{key} {value}")
                            try:
                                write_api.write(bucket=BUCKET, record=point)
                            except Exception as e:
                                print(f"Write failed. Error: {e}", file=sys.stderr)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}", file=sys.stderr)


## MQTT logic - Register callbacks and start MQTT client
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.loop_forever()