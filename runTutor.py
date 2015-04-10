import os
import os.path
import sys
import random
import time
import datetime
import collections

import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior    

from tutorMotions import *

def log_answer(data_file,number,q_type,answer,correct):
	data_file.write("Question #%d, Type: %d, Answered: %s, %s\n"%(number,q_type,answer,correct))
	data_file.flush()

def log_data(data,per,tot,cor):
	data.seek(0)
	data.truncate()
	data.write("%d\n"%per)
	data.write("%d\n"%tot)
	data.write("%d\n"%cor)

def tutor(data_file, data_1, data_2):
	count = 0
	i = 1
	new = True

	if not data_1.readline():
		per1 = 100
		tot1 = 0
		cor1 = 0
	else:
		data_1.seek(0)
		per1 = int(data_1.readline())
		tot1 = int(data_1.readline())
		cor1 = int(data_1.readline())

	if not data_2.readline():
		per2 = 100
		tot2 = 0
		cor2 = 0
	else:
		data_2.seek(0)
		per2 = int(data_2.readline())
		tot2 = int(data_2.readline())
		cor2 = int(data_2.readline())

	while i in range(1,10):
		
		correct = False

		if new == True:
			q_type = random.randint(0, 1)
			if q_type is 0:
				a = random.randint(0, 100)
				b = random.randint(0, 100)
			else:
				a = random.randint(0, 12)
				b = random.randint(0, 12)

		if q_type is 0:
			tot1 += 1
		else:
			tot2 += 1

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
			else:
				goNao.genSpeech("That's not a number!")

		if int(human_choice) == answer:
			correct = True
			new = True
			count = 0
			goNao.assess("correct")
			if q_type is 0:
				cor1 += 1
			else:
				cor2 += 1
		
		else:
			if q_type is 0:
				per1 = (float(cor1)/float(tot1)) * 100
			else:
				per2 = (float(cor2)/float(tot2)) * 100
			count = count + 1
			if count > 3:
				goNao.assess("trouble")
				break_choice = raw_input("Take a break? y for yes, n for no: ")
				if break_choice is "y":
					goNao.genSpeech("I have a fun game for you.")
					time.sleep(60)
					goNao.genSpeech("That was fun! Now let's get back to work.")
			elif q_type is 0 and per1 < 70 and tot1 > 10:
				goNao.assess("trouble_add")
			elif q_type is 1 and per2 < 70 and tot2 > 10:
				goNao.assess("trouble_mult")
			else:
				goNao.assess("wrong")

		log_answer(data_file,i,q_type,human_choice,correct)
		
		if (correct == True):
			i = i + 1

	if tot1 is not 0:
		per1 = (float(cor1)/float(tot1)) * 100
	if tot2 is not 0:
		per2 = (float(cor2)/float(tot2)) * 100
	
	log_data(data_1,per1,tot1,cor1)
	log_data(data_2,per2,tot2,cor2)
	
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
	data_file = open("data/Tony.txt","a")
	tutor(data_file)

elif(choice == "s"):
    participant_name = raw_input('Input participant\'s name: ').replace("\n","").replace("\r","")
    if os.path.exists("data/%s.txt"%participant_name):
    	data_file = open("data/%s.txt"%participant_name,"a")
    	data_1 = open("data/%s_1.txt"%participant_name,"w")
    	data_2 = open("data/%s_2.txt"%participant_name,"w")
    	data_1.close()
    	data_2.close()
    else:
    	data_file = open("data/%s.txt"%participant_name,"a")
    	data_file.write("%s\n"%participant_name)
    data_file.write("------------\n")
    today = datetime.datetime.now()
    data_file.write("%s\n" % today)
    data_file.flush()

    data_1 = open("data/%s_1.txt"%participant_name,"r+")
    data_2 = open("data/%s_2.txt"%participant_name,"r+")

    goNao.intro()
    postureProxy.goToPosture("SitRelax", 1.0)

    goNao.genSpeech("Shall we get started, %s?"%participant_name)
    time.sleep(2)

    tutor(data_file, data_1, data_2)
    postureProxy.goToPosture("SitRelax", 1.0)

    goNao.releaseNao()
    data_file.write("\n")
    data_file.close()
