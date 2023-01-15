import grpc
import location_pb2
import location_pb2_grpc
import json
import time
import os
from concurrent import futures

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""
print("Sending sample payload..")

channel = grpc.insecure_channel("localhost:30005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.LocationEventMessage(
    personId="0001",
    latitude=59.911491,
    longitude=10.757933
)
print(location)
response = stub.Create(location)
print("SENT")
print(response)

# from kafka import KafkaProducer
# TOPIC_NAME = 'locations'
# KAFKA_SERVER = 'localhost:30010'
# request_value = {
#     "personId": "0001",
#     "latitude": 59.911491,
#     "longitude": 10.757933,
# }
# producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, api_version=(0,11,5),
#                                  value_serializer=lambda v: json.dumps(v).encode('utf-8'))
# producer.send(TOPIC_NAME, request_value)
# print("SENT VLAUE")
# producer.flush()