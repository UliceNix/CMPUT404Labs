#!/usr/bin/env python

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.bind(("0.0.0.0", 8000)) # Listen to any available address
clientSocket.listen(5) # The number of connections we allow

(incomingSocket, address) = clientSocket.accept()
print "We got a connection from %s" % (str(address))

googleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
googleSocket.connect(("www.google.ca", 80))

incomingSocket.setblocking(0)
googleSocket.setblocking(0)

while True:
    skip = False
    # Forward the client to google
    try:
        part = incomingSocket.recv(1024)
    except socket.error, exception:
        if exception.errno == 11:
            skip = True
        else:
            raise
    if not skip:

        if (len(part) > 0):
            print "> " + part
            googleSocket.sendall(part)
        else:
            exit(0)
    skip = False
    try:
        # Forward from google to the client
        part = googleSocket.recv(1024)
    except socket.error, exception:
        if exception.errno == 11:
            skip = True
        else:
            raise

    if not skip:
        if (len(part) > 0):
            print "< " + part
            incomingSocket.sendall(part)
        else:
            exit(0)
