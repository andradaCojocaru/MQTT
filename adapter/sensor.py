import time
import json
import paho.mqtt.client as mqtt
from faker import Faker
from datetime import datetime

# let's connect to the MQTT broker
MQTT_BROKER_URL = "mqtt.eclipseprojects.io"

def generate_fake_mqtt_topic():
    # Generare de componente pentru locație și stație
    location = "UPB"
    station = fake.word()

    # Asigurare că componentele nu conțin caracterul special "/"
    location = location.replace("/", "_")
    station = station.replace("/", "_")

    # Formatare subiect MQTT
    mqtt_topic = f"{location}/{station}"

    return mqtt_topic

mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER_URL)

# Init faker our fake data provider
fake = Faker()

# Infinite loop of fake data sent to the Broker
while True:
    data = {
        "BAT": fake.random_int(min=0, max=100),
        "HUMID": fake.random_int(min=0, max=100),
        "PRJ": "SPRC",
        "TMP": fake.pyfloat(left_digits=2, right_digits=1),
        "status": "OK",
        "timestamp": fake.date_time_between_dates(
            datetime_start=datetime(2024, 1, 1),
            datetime_end=datetime.now()
        ).isoformat()
    }

    # sensor_data = {
    #     "timestamp": fake.date_time_this_decade().isoformat(),
    #     "temperature": fake.pyfloat(left_digits=2, right_digits=1),
    #     "humidity": fake.random_int(min=0, max=100),
    #     "pressure": fake.random_int(min=0, max=1000),
    # }


    # Convert the data dictionary to a JSON-formatted string
    payload1 = json.dumps(data)
    # payload2 = json.dumps(sensor_data)
    topic = generate_fake_mqtt_topic()

    mqttc.publish(topic, payload1)
    print(f"topic: {topic}")
    print(f"Published new temperature measurement: {payload1}")
    time.sleep(1)
    # mqttc.publish(MQTT_PUBLISH_TOPIC, payload2)
    # print(f"Published new temperature measurement: {payload2}")
    # time.sleep(1)
