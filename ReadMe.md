To run the program run "Main.py" using python3.+ version  

Example:-
python3 Main.py


System Requirements
1) Python 3.+ any version
2) Python Libraries required are:
	1)time
	2)nltk (wordnet, pos)
	3)itertools
	4)random
	5)requests
	6)base64
	7)sys
	8)os.path
	9)json
	10)copy
	11)http.client
	12)watson_developer_cloud

Note : Code is tested and work on python3+ version
 
Code makes call to Variosu Api(s) So require Internet Connection

System credentials
1) To run on your own Watson Assistant , you need to change "username, password" in line 8,9 in WatsonAssistantIntent.py file

2) To run on your own Microsoft Luis, you need to to replace subscription key on line 6 in LuisIntent.py
   you also need to change path at to your api in in Get and Post methods
 
3) To run on your own DialogFlow, 
   you need to change the Developer token at line 5 in DialogFlowIntent.py
   

  
	
	