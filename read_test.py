import os
import os.path
import sys
import random
import time
import datetime
import collections

data_1 = open("Tony_1.txt","r+")
per1 = int(data_1.readline())
per2 = int(data_1.readline())
print per1
print per2
if not data_1.readline():
	print "yes"
else:
	print "no"
a = random.randint(0, 100)
b = random.randint(0, 100)
data_1.seek(0)
data_1.truncate()
data_1.write("%s\n"%a)
data_1.write("%s\n"%b)