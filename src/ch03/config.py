"""
Module containing gRPC server default configurations.
"""
from os import environ


port  = int(environ.get('PORT', 8888))
host = environ.get('HOST', 'localhost')
