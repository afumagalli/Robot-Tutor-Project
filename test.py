import os
import os.path
import sys
import random
import time
import datetime
import collections
import socket

data = "1 0 40 55"
q_type, help, answer, human_choice = data.split(' ')
q_type = int(q_type)
help = int(help)
answer = int(answer)
human_choice = int(human_choice)
print q_type, help, answer, human_choice