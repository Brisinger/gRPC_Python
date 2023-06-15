"""
Module streaming binary string with chunk transfer encoding.
This form of encoded messages is sent via HTTP/1.1 APIs.
gRPC uses HTTP/2.0 transport mechanism that doesn't support chunk transfer encoding.
"""
from socket import socket


with open(file="request.txt", mode='rb') as fp:
    data = fp.read()
    #print(data)

# Socket connecting with httpbin.org
sock = socket()
sock.connect(('httpbin.org', 80))
sock.sendall(data)

# Chunk based encoding.
chunks = []
for chunk in iter(lambda: sock.recv(1024), b''):
    chunks.append(chunk)
# storing the reply by cncating all the chunks.
REPLY = b''.join(chunks)
print(REPLY.decode())
