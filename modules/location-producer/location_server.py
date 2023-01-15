import json
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

print("HELLO")
class LocationServicer(location_pb2_grpc.LocationServiceServicer):

    def Create(self, request, context):
        print("received message")
        print(request)
        request_value = {
            "personId": request.personId,
            "latitude": request.latitude,
            "longitude": request.longitude,
        }
        print(request_value)
        self._push_request_to_kafka(request_value)
        return location_pb2.LocationEventMessage(**request_value)

    @staticmethod
    def _push_request_to_kafka(request_value):

        producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER], api_version=(0,11,5),
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        try:
            print("pushing to que")
            producer.send(TOPIC_NAME, request_value)
            producer.flush()
            print("pushing to succeeded")
        except KafkaError as e:
            print('Not able to send message to server', e)
            pass


# Initialize gRPC server
print("Starting server on port 5005")
print(KAFKA_SERVER)
print(TOPIC_NAME)
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
server.add_insecure_port("[::]:5005")
server.start()
print("Server started")
# Keep thread alive
try:
    print(".")
    while True:
        time.sleep(500)
except KeyboardInterrupt:
    server.stop(0)
