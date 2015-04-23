#!/usr/bin/env python

import socket
import random

TCP_IP = '127.0.0.1'
TCP_PORT = 5006
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print 'Waiting for client connection...'

conn, addr = s.accept()
print 'Connection address:', addr
data = conn.recv(BUFFER_SIZE)
print "received data:", data

i=1
while i in range(1,10):
    a = random.randint(0, 12)
    b = random.randint(0, 12) 
    
    #get user's answer
    human_choice = raw_input("What is %d * %d? "%(a, b))
    #assemble message in correct format
    data = 'Question ' + str(i) + ': ' + human_choice +'\n' 
    #send to client
    conn.send(data)  # echo
    i = i+1

raw_input("Press enter to end session.")
data = 'exit'
conn.send(data)   
conn.close()