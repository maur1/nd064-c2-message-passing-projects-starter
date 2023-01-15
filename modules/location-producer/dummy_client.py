import grpc
import location_pb2
import location_pb2_grpc

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
response = stub.Create(location)
print("Payload sent")
