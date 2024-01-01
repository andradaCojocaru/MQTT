"""
MQTT subscriber - Listen to a topic and sends data to InfluxDB
"""

from datetime import datetime
import json
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
        return isinstance(json_object, dict)  # Verificăm dacă este un obiect JSON de tip dict
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
                # Parse the JSON payload
                data = json.loads(msg.payload.decode("utf-8"))

                # Extract relevant fields
                #temperature = max(float(data.get("TMP", 0)), 0.0)  # Ensure temperature is non-negative
                # location = data.get("location", "Unknown")
                timestamp = data.get("timestamp")
                if timestamp is None:
                    timestamp = datetime.now()
                    print(f"Datatime: now")
                else:
                    print(f"Datatime: {timestamp}")
                location, station = extract_location_and_station(msg.topic)
                point = Point("msg.topic")
                #.tag("location", location).tag("station", station)
                print(f"location: {location}, station: {station}")

                #point.time(timestamp, WritePrecision.S)

                # Adăugarea câmpurilor numerice la punct
                for key, value in data.items():
                    if isinstance(value, (int, float)):
                        point.field(key, value)
                        print(f"adauagte: {key}, {value}")

                # Scrierea în InfluxDB
                print(f"BUCKET: {BUCKET}")
                try:
                    write_api.write(bucket=BUCKET, record=point)
                    print("Write successful")
                except Exception as e:
                    print(f"Write failed. Error: {e}")

                # # InfluxDB logic
                # point = Point(MQTT_PUBLISH_TOPIC).tag("location", location).field("temperature", temperature)
                # write_api.write(bucket=BUCKET, record=point)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")


## MQTT logic - Register callbacks and start MQTT client
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.loop_forever()