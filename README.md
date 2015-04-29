# Robot-Tutor-Project
Senior project for CPSC 490 to code an adaptive robot tutor using a contextual bandit approach
<p>
<b>Instructions:</b> <p>
1) Install naoqi Python SDK (see instructions here: http://doc.aldebaran.com/1-14/dev/python/install_guide.html) <p>
2) Turn on Nao and get IP address (press center button). Make sure IP in ip.txt is correct.<p>
3) If using TCP, establish your TCP server (for demo, run the tutor_TCPserver.py file)
   Run the runTutor.py or runTutorWithTCP.py file in Python <p>
4) Select s to start a tutroing interaction <p>
5) Answer questions in Terminal or through your TCP server <p>
<p>
<b>Note:</b> If using a new topics.txt list, all previous data in the ./data or ./data_TCP folder must be wiped for accuracy
<p>
<b>Important information on data files:</b>
Student history is stored in the ./data or ./data_TCP folder. Each participant gets a file created for them when they interact with the robot for the first time. In the participant_name.txt file, all tutoring interactions are recorded. Each session is marked with the date and time the user began the intraction. 
<b>Future additions:</b><p>
-Use of affect detection as feature vector<p>
-Database of hints for use in all question types<p>
-Broadening of animacy strings<p>
