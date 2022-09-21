import Adafruit_DHT
import time
from datetime import datetime
import os

from digitalio import DigitalInOut, Direction
from psycopg2.extras import execute_values
import board
import psycopg2  # database adapter

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_GPIO_PIN = 4
print("Collecting Temperature and Humidity data/n")

connection_string = os.environ.get(
    "TIMESCALEDB_CONNECTION", default="dbname=tsdb user=tsdbadmin"
)

with psycopg2.connect(connection_string) as conn:
    with conn.cursor() as cur:  # executes postgresql commands in db session
        while True:
            values = []
            humid, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_GPIO_PIN)
            if humid is not None and temp is not None:
                print(
                    "Temperature : {0:0.2f}C   Humidity : {1:0.2f}%".format(temp, humid)
                )
                values.append((datetime.utcnow(), temp, humid))

            else:
                print("Data could not be collected")

            time.sleep(30)
            execute_values(
                cur,  # cur to use to execute query
                "INSERT INTO dht11(time, temperature, humidity) VALUES %s",
                values,
            )
            conn.commit()
