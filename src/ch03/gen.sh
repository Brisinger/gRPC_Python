#!/bin/bash
"""
Module to execute command on shell terminal
-I : Option to search for .proto protobuf definition file within current directory specified by dot(.)
-m : Module to be executed.
-python_out : Generates python module by serilizing protobuf types defined in .proto file
-grpc_python_out : Generates gRPC service classes for I/O.
"""
# Make it an executable by running the command chmod +x gen.sh in current directory containing the shell file.
python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    rides.proto