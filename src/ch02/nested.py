"""
Module that uses the message type containing location as a nested type.
"""
import rides_pb2 as pb

loc = pb.Location(
    lat = 32.5270941,
    lng = 34.9404309,
)
print(loc)

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
# Show the entire request as class serialized based on .proto file.
print(request)

# Access latitude on the serialized message type request from nested type Location.
print(f"Latititude: {request.location.lat}")
