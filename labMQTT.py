import paho.mqtt.client as mqtt
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test/#")
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("broker.hivemq.com", 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
 
try:
    while True:
        # Citire mesaj de la tastatură și trimitere pe topicul propriu
        user_input = input()
        client.publish("/test/Ada", user_input)
except KeyboardInterrupt:
    print("\nAplicația se închide.")
    client.disconnect()
    client.loop_stop()






# import paho.mqtt.client as mqtt
# from influxdb import InfluxDBClient
# import json
# from datetime import datetime

# # Configurare client MQTT
# mqtt_broker_host = "mqtt-broker"  # Numele serviciului brokerului MQTT în Docker Swarm
# mqtt_broker_port = 1883
# mqtt_topic = "#"

# # Configurare client InfluxDB
# influxdb_host = "influxdb"  # Numele serviciului InfluxDB în Docker Swarm
# influxdb_port = 8086
# influxdb_database = "mydb"

# def on_connect(client, userdata, flags, rc):
#     print("Conectat la broker MQTT cu codul de retur: " + str(rc))
#     client.subscribe(mqtt_topic)

# def on_message(client, userdata, msg):
#     payload = msg.payload.decode("utf-8")
#     try:
#         data = json.loads(payload)
#         process_data(data)
#     except json.JSONDecodeError as e:
#         print(f"Eroare la decodificarea JSON: {e}")

# def process_data(data):
#     # Realizati aici logica pentru a adauga datele in InfluxDB
#     timestamp = data.get("timestamp", get_current_timestamp())
#     for key, value in data.items():
#         if key != "timestamp" and isinstance(value, (int, float)):
#             write_to_influxdb(key, value, timestamp)

# def write_to_influxdb(measurement, value, timestamp):
#     json_body = [
#         {
#             "measurement": measurement,
#             "time": timestamp,
#             "fields": {"value": value}
#         }
#     ]
#     try:
#         influx_client.write_points(json_body)
#     except Exception as e:
#         print(f"Eroare la scrierea in InfluxDB: {e}")

# def get_current_timestamp():
#     return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

# # Configurare client MQTT
# mqtt_client = mqtt.Client()
# mqtt_client.on_connect = on_connect
# mqtt_client.on_message = on_message

# # Configurare client InfluxDB
# influx_client = InfluxDBClient(host=influxdb_host, port=influxdb_port)
# influx_client.switch_database(influxdb_database)

# # Conectare la brokerul MQTT
# mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)

# # Asteapta evenimente MQTT
# mqtt_client.loop_forever()

# import paho.mqtt.client as mqtt
# from influxdb import InfluxDBClient
# import json
# from datetime import datetime

# # Configurați adresa și portul brokerului MQTT
# mqtt_broker_host = "mqtt-broker"  # Înlocuiți cu adresa corectă
# mqtt_broker_port = 1883

# # Configurați adresa și portul InfluxDB
# influxdb_host = "influxdb"  # Înlocuiți cu adresa corectă
# influxdb_port = 8086
# influxdb_database = "mydb"

# # Configurați clientul MQTT
# mqtt_client = mqtt.Client()

# # Configurați clientul InfluxDB
# influx_client = InfluxDBClient(host=influxdb_host, port=influxdb_port)
# influx_client.switch_database(influxdb_database)

# # Funcție pentru procesarea mesajelor
# def process_message(client, userdata, msg):
#     payload = msg.payload.decode("utf-8")
#     try:
#         data = json.loads(payload)
#         process_data(data)
#     except json.JSONDecodeError as e:
#         print(f"Eroare la decodificarea JSON: {e}")

# # Funcție pentru procesarea datelor și scrierea în InfluxDB
# def process_data(data):
#     timestamp = data.get("timestamp", get_current_timestamp())
#     for key, value in data.items():
#         if key != "timestamp" and isinstance(value, (int, float)):
#             write_to_influxdb(key, value, timestamp)

# # Funcție pentru scrierea în InfluxDB
# def write_to_influxdb(measurement, value, timestamp):
#     json_body = [
#         {
#             "measurement": measurement,
#             "time": timestamp,
#             "fields": {"value": value}
#         }
#     ]
#     try:
#         influx_client.write_points(json_body)
#     except Exception as e:
#         print(f"Eroare la scrierea în InfluxDB: {e}")

# # Funcție pentru obținerea timestamp-ului curent
# def get_current_timestamp():
#     return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

# # Setarea funcției de procesare a mesajelor la evenimentul on_message
# mqtt_client.on_message = process_message

# # Conectarea la brokerul MQTT și abonarea la toate mesajele
# mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)
# mqtt_client.subscribe("#")  # Abonare la toate mesajele (topic wildcard - #)

# # Așteptarea evenimentelor MQTT
# mqtt_client.loop_forever()
