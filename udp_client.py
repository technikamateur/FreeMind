#!/usr/bin/python

import socket, time #import socket module
while True:
    s = socket.socket() #create a socket object
    host = '192.168.2.112' #Host i.p
    port = 12397 #Reserve a port for your service
    message = "lol"
    s.connect((host,port))
    print(s.recv(1024))
    s.sendto(message.encode(),(host, port))
    s.close
#This code is probably good for Python 2. But in Python 3, this will cause an issue, something related to bit encoding. I was trying to make a simple TCP server and encountered the same problem. Encoding worked for me. Try this with sendto command.
#
#clientSocket.sendto(message.encode(),(serverName, serverPort))
#
#Similarly you would use .decode() to receive the data on the UDP server side, if you want to print it exactly as it was sent.
