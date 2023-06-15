"""
Module to validate the request data to gRPC server.
"""
class Error(ValueError):
    """
    Customized ValueError exception class.
    """
    def __init__(self, field, reason):
        super().__init__(f'{field}: {reason}')
        self.field = field
        self.reason = reason


def start_request(request):
    """
    Check if request data for the protbuf definition field is not empty.
    """
    if not request.driver_id:
        raise Error('driver_id', 'empty')
    # TODO: Validate more data fields in request
