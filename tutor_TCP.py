#!/usr/bin/env python

import socket
import random

from tutorMotions import *

#Get the Nao's IP
ipAdd = None
try:
    ipFile = open("ip.txt")
    ipAdd = ipFile.readline().replace("\n","").replace("\r","")
except Exception as e:
    print "Could not open file ip.txt"
    ipAdd = raw_input("Please write Nao's IP address... ") 


#Try to connect to it
goNao = None
try:
    goNao = Gesture(ipAdd, 9559)
except Exception as e:
    print "Could not find nao. Check that your ip is correct (%s)" %ipAdd
    sys.exit()


#Set postureProxy
try:
    postureProxy = ALProxy("ALRobotPosture", ipAdd, 9559)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e


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
print data

#example with ten simple multiplication questions
i = 1
new = True
while i in range(1,11):

	help = 0

	if new == True:
		q_type = random.randint(0, 1)
		if q_type is 0:
			a = random.randint(0, 100)
			b = random.randint(0, 100)
		else:
			a = random.randint(0, 12)
			b = random.randint(0, 12)

	new = False
	val = False
		
	while not val:
		if q_type is 0:
			goNao.genSpeech("What is %d plus %d?"%(a, b))
			time.sleep(2)
			answer = a + b
			human_choice = raw_input("What is %d + %d? "%(a, b))
		else:
			goNao.genSpeech("What is %d times %d?"%(a, b))
			time.sleep(2)
			answer = a * b
			human_choice = raw_input("What is %d * %d? "%(a, b))
		if human_choice.isdigit():
			val = True
		elif human_choice == "h":
			help = 1
		else:
			goNao.genSpeech("That's not a number!")

	q_type_s = str(q_type)
	help_s = str(help)
	answer_s = str(answer)

	data = q_type_s + " " + help_s + " " + answer_s + " " + human_choice
	conn.send(data) #send to client
	if int(human_choice) == answer:
		new = True
		i = i + 1

raw_input("Press enter to end session.")
data = 'exit'
conn.send(data)   
conn.close()