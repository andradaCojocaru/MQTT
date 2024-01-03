import time
import json
import paho.mqtt.client as mqtt
from faker import Faker
from datetime import datetime

# let's connect to the MQTT broker
MQTT_BROKER_URL = "mqtt.eclipseprojects.io"

def generate_fake_mqtt_topic():
    location = "UPB"
    station = fake.word()

    location = location.replace("/", "_")
    station = station.replace("/", "_")

    mqtt_topic = f"{location}/{station}"

    return mqtt_topic

def generate_fake_data():
    return {
        "BAT": fake.random_int(min=0, max=100),
        "HUMID": fake.random_int(min=0, max=100),
        "PRJ": "SPRC",
        "TMP": fake.pyfloat(left_digits=2, right_digits=1),
        "status": "OK",
        "timestamp": fake.date_time_between_dates(
            datetime_start=datetime(2024, 1, 3),
            datetime_end=datetime.now()
        ).isoformat()
    }

mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER_URL)

fake = Faker()

while True:
    
    topic = generate_fake_mqtt_topic()

    for _ in range(10):
        payload = generate_fake_data()

        mqttc.publish(topic, json.dumps(payload))
        print(f"topic: {topic}")
        print(f"Published new temperature measurement: {json.dumps(payload)}")
        time.sleep(1)
