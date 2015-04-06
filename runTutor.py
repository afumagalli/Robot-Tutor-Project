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

def tutor(data_file):
	count = 0
	i = 1
	new = True
	global add_per, mult_per
	global add_cor, mult_cor
	global add_tot, mult_tot
	add_per = 100
	mult_per = 100
	add_cor = 0
	mult_cor = 0
	add_tot = 0
	mult_tot = 0

	while i in range(1,8):
		
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
			add_tot += 1
		else:
			mult_tot += 1

		new = False

		val = False
		while not val:
			if q_type is 0:
				goNao.genSpeech("What is %d + %d?"%(a, b))
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
				add_cor += 1
			else:
				mult_cor += 1
		else:
			if q_type is 0:
				add_per = (add_cor/add_tot) * 100
			else:
				mult_per = (mult_cor/mult_tot) * 100
			count = count + 1
			if count > 3:
				goNao.assess("trouble")
				break_choice = raw_input("Take a break? y for yes, n for no: ")
				if break_choice is "y":
					goNao.genSpeech("I have a fun game for you.")
					time.sleep(60)
					goNao.genSpeech("That was fun! Now let's get back to work.")
			elif q_type is 0 and add_per < 70 and add_tot > 3:
				goNao.assess("trouble_add")
			elif q_type is 1 and mult_per < 70 and mult_tot > 3:
				goNao.assess("trouble_mult")
			else:
				goNao.assess("wrong")

		log_answer(data_file,i,q_type,human_choice,correct)
		
		if (correct == True):
			i = i + 1

	if add_tot is not 0:
		add_per = (float(add_cor)/float(add_tot)) * 100
	if mult_tot is not 0:
		mult_per = (float(mult_cor)/float(mult_tot)) * 100
	data_file.write("Addition: %d\n"%add_per)
	data_file.write("Multiplication: %d\n"%mult_per)
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
    else:
    	data_file = open("data/%s.txt"%participant_name,"a")
    	data_file.write("%s\n"%participant_name)
    data_file.write("------------\n")
    today = datetime.datetime.now()
    data_file.write("%s\n" % today)
    data_file.flush()

    goNao.intro()
    postureProxy.goToPosture("SitRelax", 1.0)

    goNao.genSpeech("Shall we get started, %s?"%participant_name)
    time.sleep(2)

    tutor(data_file)
    postureProxy.goToPosture("SitRelax", 1.0)

    goNao.releaseNao()
    data_file.write("\n")
    data_file.close()
