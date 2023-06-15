"""
Module working with TimeStamp data from Google's Protocol buffer.
"""
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
import rides_pb2 as pb

# Generate serialized python request object.
request = pb.StartRequest(
    car_id = 95,
    driver_id = 'McQueen',
    passenger_ids = ['p1', 'p2', 'p3'],
    type = pb.POOL,
    location = pb.Location(
        lat = 32.5270941,
        lng = 34.9404309,
    ),
)
# The request doesn't contain time data whose type differs from python's datetime type.
# Instantiate Python's datetime type data.
time = datetime(2022, 2, 12, 14, 39, 42)
# Parse the python's datetime object to google's protocol buffer Timestamp type of data nested in request.
request.time.FromDatetime(time)
# Display the serialized python request from protocol buffer.
print(request)

# Convert the request time data to python datetime object.
# region ToDatetime
time2 = request.time.ToDatetime()
print(type(time2), time2)
# endregion

# region now
now = Timestamp()
now.GetCurrentTime()
print(type(now), now)
# endregion
