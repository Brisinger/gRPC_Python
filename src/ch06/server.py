"""
Module that starts the server through gRPC generated servicer asynchronously.
"""
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
from uuid import uuid4
# Adding gRPC reflection to server.
from grpc_reflection.v1alpha import reflection
import grpc
import config
import log
import rides_pb2 as pb
import rides_pb2_grpc as rpc
import validate


def new_ride_id() -> str:
    """
    Generates a random UUID uniquely identifying a ride.

    Returns:
    --------
        str: Hexadecimal base64 encoded string uniquely identifying a ride request.
    """
    return uuid4().hex

class TimingInterceptor(grpc.ServerInterceptor):
    """
    Class intercepting rpc calls on the service side.
    It intercepts RPC's by overriding ServerInterceptor and benchmarks their performance.
    
    
    Methods:
    -----
       intercept_service(self, continuation, handler_call_details): intercept incoming RPCs.
    """
    def intercept_service(self, continuation, handler_call_details):
        """
        Intercepts and benchmarks performance of rpc's.
        It computes the duration taken to execute current rpc.


        Args:
        -----
            continuation: Continuation invoking the next rpc in chain.
            handler_call_details: Result from subsequent rpc invocation.
        """
        start = perf_counter()
        try:
            return continuation(handler_call_details)
        finally:
            duration = perf_counter() - start
            name = handler_call_details.method
            log.info('%s took %.3fseconds', name, duration)


class Rides(rpc.RidesServicer):
    """
    Implements the gRPC generated service code by overriding it's Start and Track streaming method.

    Methods:
    --------
        Start(request, context): Starts the rides service generated by gRPC service type.
        Track(request_iterator, context): Streams location requests to gRPC server.
    """
    def Start(self, request, context) -> pb.StartResponse:
        """
        Starts a new ride service.

        
        Args:
        -----
        request: The request to service from client.
        context: The context to set statuscodes and details on gRPC or cancel RPC call.

        Returns:
        --------
            StartResponse: Response containing ride request id.
        """
        log.info('ride: %r', request)

        try:
            validate.start_request(request)
        except validate.Error as err:
            log.error('bad request: %s', err)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'{err.field} is {err.reason}')
            raise err

        # TODO: Store ride in database
        ride_id = new_ride_id()
        return pb.StartResponse(id=ride_id)

    def Track(self, request_iterator, context) -> pb.TrackResponse:
        """
        Track the ride requests location streamed to the server


        Args:
        ----
            request_iterator (iter(streaming requests): Iteration of requests streamed.
            context: The context to set statuscodes and details on gRPC or cancel RPC call.
        
        Returns:
        --------
            TrackResponse: Response containing no. of requests streamed.
        """
        count = 0
        for request in request_iterator:
            # TODO Store in database
            log.info('Track %s', request)
            count += 1
        return pb.TrackResponse(count=count)

def load_credentials():
    """
    Load the security credentials from private key and certificate.


    Returns:
    --------
    A ServerCredentials for use with an SSL-enabled Server. 
    Typically, this object is an argument to add_secure_port() method during server setup.
    """
    # Read certification file.
    with open(file=config.cert_file, mode='rb') as fp:
        cert = fp.read()
    # Read private key.
    with open(file=config.key_file, mode='rb') as fp:
        key = fp.read()

    return grpc.ssl_server_credentials([(key, cert)])

def build_server(port:int):
    """
    Builds the gRPC server instance binding to given port.


    Args:
    -----
        port (int): The port number on which server starts.

    Returns:
    --------
        The configured server with given address port.
    """
    # Create a generic gRPC server with ThreadPoolExecutor.
    _server = grpc.server(ThreadPoolExecutor(), interceptors=[TimingInterceptor(),])
    # Register server to gRPC server providing RidesServicer.
    rpc.add_RidesServicer_to_server(Rides(), _server)
    # Use gRPC reflection to query methods and types available in server.
    names = (
        pb.DESCRIPTOR.services_by_name['Rides'].full_name,
        reflection.SERVICE_NAME,
    )
    # Enable reflection
    reflection.enable_server_reflection(names, _server)

    addr = f'[::]:{port}'
    # gRPC uses HTTPS/2.0 to transfer data in-wire by default.
    # Connect to gRPC server using HTTPS/2.0 secure port.
    # credentials = load_credentials()
    # _server.add_secure_port(addr, credentials)
    _server.add_insecure_port(address=addr)
    return _server


if __name__ == '__main__':
    # Server instance
    server = build_server(config.port)
    server.start()
    log.info('server ready on %s', config.port)
    server.wait_for_termination()