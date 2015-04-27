import os
import os.path
import sys
import random
import time
import datetime
import collections
import socket

import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior    

from tutorMotions import *

def log_answer(history,number,q_type,answer,correct):
	history.write("Question #%d, Type: %d, Answered: %s, %s\n"%(number,q_type,answer,correct))
	history.flush()

def log_data(data,per,tot,cor):
	data.seek(0)
	data.truncate()
	data.write("%d\n"%per)
	data.write("%d\n"%tot)
	data.write("%d\n"%cor)

def tutor(history, data, categ):
	i = 1
	new = True
	wrong = []
	per = []
	tot = []
	cor = []

	TCP_IP = '127.0.0.1'
	TCP_PORT = 5006
	BUFFER_SIZE = 1024
	MESSAGE = "Session started!"

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(MESSAGE)

	for j in range(categ):
		wrong.append(0)
		if not data[j].readline():
			per.append(100)
			tot.append(0)
			cor.append(0)
		else:
			data[j].seek(0)
			per.append(int(data[j].readline()))
			tot.append(int(data[j].readline()))
			cor.append(int(data[j].readline()))

	while 1:
		msg = s.recv(BUFFER_SIZE)
		if not msg:
			break
		if (msg == "exit"):
			break
		q_type, help, answer, human_choice = msg.split(' ')
		q_type = int(q_type)
		help = int(help)
		answer = int(answer)
		human_choice = int(human_choice)

		correct = False
		tot[q_type] += 1

		if human_choice == answer:
			correct = True
			wrong[q_type] = 0
			cor[q_type] += 1
			goNao.assess("correct")

		elif help:
			tot[q_type] -= 1
			per[q_type] = (float(cor[q_type])/float(tot[q_type])) * 100
			
			if per[q_type] > 70:
				goNao.genSpeech("I think you can do it. Try to answer.")
			
			else:
				goNao.assess("hint")
		
		else:
			per[q_type] = (float(cor[q_type])/float(tot[q_type])) * 100
			wrong[q_type] = wrong[q_type] + 1
			
			if wrong[q_type] > 4:
				goNao.assess("trouble")
				break_choice = raw_input("Take a break? y for yes, n for no: ")
				if break_choice is "y":
					goNao.genSpeech("I have a fun game for you.")
					time.sleep(60) # play a game
					goNao.genSpeech("That was fun! Now let's get back to work.")
			
			elif per[q_type] < 70 and tot[q_type] > 10:
				goNao.assess("hint")
				hint_choice = raw_input("Would you like a hint? y for yes, n for no: ")
				if hint_choice is "y":
					goNao.genSpeech("I think I can help")
					# give a hint

			elif per[q_type] > 70 and tot[q_type] > 10:
				goNao.assess("confused")
			
			else:
				goNao.assess("wrong")

		log_answer(history,i,q_type,human_choice,correct)
	
	for i in range(categ):
		if tot[i] is not 0:
			per[i] = (float(cor[i])/float(tot[i])) * 100
		log_data(data[i],per[i],tot[i],cor[i])
	
	goNao.goodbye()


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


#Choose an action
#Set all the possible commands
commands=collections.OrderedDict((("i","Run the intro"),
("r","Release motors"),
("t","Test new code"),
("s","Start tutoring interaction")
))


#Output all the commands
print "\nPlease choose an action:"
for key,value in commands.items():
    print("\t%s => %s"%(key,value))


#Have the user select the choice
choice = ""
if choice not in commands:
    choice = raw_input('Choice: ').replace("\n","").replace("\r","")


#Execute the user's choice
if(choice == "i"):
    postureProxy.goToPosture("Stand", 1.0)
    goNao.intro()

elif(choice=="r"):
    goNao.releaseNao()

elif(choice == "t"):
	history = open("data/Tony.txt","a")
	tutor(history)

elif(choice == "s"):
    participant_name = raw_input('Input participant\'s name: ').replace("\n","").replace("\r","")
    
    with open('topics.txt') as f:
    	categ = sum(1 for _ in f)
    if categ != 2:
    	print "Error"
    	exit()

    data = []
    
    if os.path.exists("data_TCP/%s.txt"%participant_name):
    	history = open("data_TCP/%s.txt"%participant_name,"a")
    
    else:
    	history = open("data_TCP/%s.txt"%participant_name,"a")
    	history.write("%s\n"%participant_name)
    	for i in range(categ):
    		open("data_TCP/%s_%d.txt"%(participant_name,i),"w")
    
    history.write("------------\n")
    today = datetime.datetime.now()
    history.write("%s\n" % today)
    history.flush()

    for i in range(categ):
    	data.append(open("data_TCP/%s_%d.txt"%(participant_name,i),"r+"))

    #goNao.intro()
    postureProxy.goToPosture("SitRelax", 1.0)

    goNao.genSpeech("Shall we get started, %s?"%participant_name)
    time.sleep(2)

    tutor(history, data, categ)
    postureProxy.goToPosture("SitRelax", 1.0)

    goNao.releaseNao()
    history.write("\n")
    history.close()
