# Robot-Tutor-Project
Senior project for CPSC 490 to code an adaptive robot tutor using a contextual bandit approach
<p>
<b>Instructions:</b> <p>
1a) Install naoqi Python SDK (see instructions here: http://doc.aldebaran.com/1-14/dev/python/install_guide.html) <p>
1b) Install easygui (see instructions here: http://sourceforge.net/projects/easygui/files/0.97/) <p>
2) Turn on Nao and get IP address (press center button). Make sure IP in ip.txt is correct.<p>
3a) If using TCP, establish your TCP server (for demo, run the tutor_TCPserver.py file)<p>
3b) Run the runTutor.py or runTutorWithTCP.py file in Python <p>
4) Select s to start a tutroing interaction <p>
5) Answer questions in Terminal or through your TCP server <p>
<b>Important information on data files:</b>
<p>
Student history is stored in the ./data or ./data_TCP folder. Each participant gets a file created for them when they interact with the robot for the first time. In the name.txt file, all tutoring interactions are recorded. Each session is marked with the date and time the user began the interaction. The question type, student answer, and whether the answer was correct are then logged for each question the student is asked. The question type is an integer value determined by iterating from 0 through the lines in the topics.txt file.
<p>
Additional data files are used to track student performance over time. These files are in the form of name_type#.txt where type# is the question type. These files consist of three numbers: the percentage of questions of that type that have been answered correctly, the total number of questions of that type that have been asked, and the total number of questions of that type that have been answered correctly. This information is accessed at the beginning of each tutoring interaction and is updated throughout the session. It is then written to the data file at the end of the session.
<p>
<b>Note:</b> If using a new topics.txt list, all previous data in the ./data or ./data_TCP folder must be wiped for accuracy
<p>
<b>Future additions:</b><p>
-Use of affect detection as feature vector<p>
-Database of hints for use in all question types<p>
-Broadening of animacy strings<p>
