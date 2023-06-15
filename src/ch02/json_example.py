"""
Module to serialize types generated from protocol buffers to json.
"""
from datetime import datetime
from google.protobuf.json_format import MessageToJson
import rides_pb2 as pb


# Message type of protocol buffer serialized to python request class
request = pb.StartRequest(
    car_id = 95,
    driver_id = "McQueen",
    passenger_ids = ["p1", "p2", "p3"],
    type = pb.POOL,
    location = pb.Location(
        lat = 32.5270941,
        lng = 34.9404309,
    ),
)
# Instance of python datetime object
time = datetime(2022, 2, 13, 14, 39, 42)
# Python datetime type set as protobuf Timestamp data type nested as time field in request.
request.time.FromDatetime(time)

# region json
# Serializing protobuf generated python request class to json
# Do not use the standard library's json use the json format library from google's protobuf
# This json formatter library knows how to deal with protocol buffer language message types
# The time data from protobuf message gets formatted as a string not as a embeded type
data = MessageToJson(request)
print("Type:", type(data))
print(data)
# endregion

# region size
# Size of converted json data from protobuf message type.
print("encode size")
print("- json data  :", len(data))
# Serialize request type from protobuf message to binary byte string.
# The length is 1/4th the size of json data sent over network.
print("- protobuf message :", len(request.SerializeToString()))
# endregion
