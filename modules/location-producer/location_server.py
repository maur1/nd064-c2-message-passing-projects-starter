import json
import logging
import time
import os
from concurrent import futures

import grpc
from kafka.errors import KafkaError

import location_pb2_grpc
import location_pb2
from kafka import KafkaProducer

TOPIC_NAME = os.getenv("KAFKA_TOPIC")
KAFKA_SERVER = os.getenv("KAFKA_URL")

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

class LocationServicer(location_pb2_grpc.LocationServiceServicer):

    def Create(self, request, context):
        logger.info(f"received msg from grpc-client: {request}")
        request_value = {
            "personId": request.personId,
            "latitude": request.latitude,
            "longitude": request.longitude,
        }
        self._push_request_to_kafka(request_value)
        return location_pb2.LocationEventMessage(**request_value)

    @staticmethod
    def _push_request_to_kafka(request_value):

        producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER], api_version=(0,11,5),
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        try:
            logger.info(f"pushing msg to kafka on TOPIC: {TOPIC_NAME}, CLUSTER: {KAFKA_SERVER}")
            producer.send(TOPIC_NAME, request_value)
            producer.flush()
            logger.info("push success")
        except KafkaError as e:
            logger.error('Not able to push message:', e)
            pass


# Initialize gRPC server
logger.info("Starting server on port 5005")
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
server.add_insecure_port("[::]:5005")
server.start()
logger.info("Server started")
# Keep thread alive
try:
    while True:
        time.sleep(500)
except KeyboardInterrupt:
    server.stop(0)
