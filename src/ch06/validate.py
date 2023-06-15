"""
Module to validate request data sent to gRPC server.
"""


class Error(ValueError):
    """
    Customized ValueError Exception.
    """
    def __init__(self, field, reason) -> None:
        super().__init__(f'{field}: {reason}')
        self.field = field
        self.reason = reason

def start_request(request):
    """
    Checks if data in request is not empty.
    """
    if not request.driver_id:
        raise Error('driver_id', 'empty')
    # TODO Validate more fields
