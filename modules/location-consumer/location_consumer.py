import logging

from kafka import KafkaConsumer
import os
import json
from sqlalchemy import create_engine

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
KAFKA_SERVER = os.environ["KAFKA_URL"]
TOPIC = os.environ["KAFKA_TOPIC"]

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

locations = KafkaConsumer(TOPIC, bootstrap_servers=[KAFKA_SERVER], api_version=(0, 11, 5), group_id=None,
                          auto_offset_reset='earliest')


def write_in_db(location):
    db_engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
    connection = db_engine.connect()
    person_id = int(location["personId"])
    lat, lon = int(location["latitude"]), int(location["longitude"])
    table_insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))" \
        .format(person_id, lat, lon)
    try:
        connection.execute(table_insert)
        logger.info("Inserted msg to db")
    except Exception as e:
        logger.error(f"Failed to insert msg to db: {e}")


for location in locations:
    message = location.value.decode('utf-8')
    location_message = json.loads(message)
    logger.info(f"Received location message: {location_message}")
    write_in_db(location_message)
