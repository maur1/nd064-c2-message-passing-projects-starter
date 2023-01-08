import json
import os
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from geoalchemy2.functions import ST_AsText, ST_Point


DB_USERNAME = "ct_admin" #os.environ["DB_USERNAME"]
DB_PASSWORD = "d293aW1zb3NlY3VyZQ==" #os.environ["DB_PASSWORD"]
DB_HOST = "postgres" #os.environ["DB_HOST"]
DB_PORT = "5432" #os.environ["DB_PORT"]
DB_NAME = "geoconnections" #os.environ["DB_NAME"]

KAFKA_SERVER = "localhost:9092" # os.environ["KAFKA_URL"]
TOPIC = "location" #os.environ["KAFKA_TOPIC"]


locations = KafkaConsumer(TOPIC, bootstrap_servers=[KAFKA_SERVER], group_id=None, auto_offset_reset='earliest')


def write_in_db(location):
    db_engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
    connection = db_engine.connect()

    person_id = location["personId"]
    coordinate = ST_Point(location["latitude"], location["longitude"])
    db_query = "INSERT INTO location (person_id, coordinate) VALUES ({}, {})" \
        .format(person_id, coordinate)
    print(db_query)
    connection.execute(db_query)


for location in locations:
    message = location.value.decode('utf-8')
    location_message = json.loads(message)
    print(location_message)
    write_in_db(location_message)