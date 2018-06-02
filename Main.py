import LuisIntent as microsoft
import DialogFlowIntent as google
import WatsonAssistantIntent as ibm
import time
import ThesisData as td

def resetApplication():
    microsoft.resetApplication()
    google.resetApplication()
    ibm.resetApplication()
    td.resetApplication()
    print("MAIN APPLICATION RESET DONE")

def getIntentList():

    temp = microsoft.getIntentList()
    print("INTENTS IN MICROSOFT LUIS:")
    for intent in temp:
        print(intent["name"])
    print("-"*25)
    temp = google.getIntentList()
    print("INTENTS IN GOOGLE DF:")
    for key in temp.keys():
            print(key)
    print("-" * 25)

    temp = ibm.getIntentList()
    print("INTENTS IN WATSON ASSISTANT:")
    temp=temp["intents"]
    for intent in temp:
            print(intent["intent"])
    print("-" * 25)

def createIntent(name):
    microsoft.createIntent(name)
    google.createIntent(name)
    ibm.createIntent(name)
    td.createIntent(name)

def add_utterance(text,intent):
    microsoft.luis.add_utterance(text,intent)
    google.add_utterance(text,intent)
    ibm.add_utterance(text,intent)
    microsoft.publish()
    td.add_utterance(text,intent)

def add_utterances(text,intent):
    microsoft.luis.add_utterances(text,intent)
    google.add_utterances(text,intent)
    ibm.add_utterances(text,intent)
    microsoft.publish()
    td.add_utterances(text,intent)

def getPrediction(userInput):
    microsoft_reply = microsoft.getPrediction(userInput)
    microsoft_reply = microsoft_reply["topScoringIntent"]
    print("Prediction on Microsoft Luis")
    if (microsoft_reply["intent"].startswith("None")):
        print("Intent : No User Defined Intent Found ", "Score : ", microsoft_reply["score"])
    else:
        print("Intent : ", microsoft_reply["intent"], " Score : ",microsoft_reply["score"])
    google_reply = google.getPrediction(userInput)
    print("Prediction on Google DialogFlow")
    if(google_reply["result"]["metadata"]["intentName"].startswith("Default Fallback")):
        print("Intent : No User Defined Intent Found ", "Score : ", google_reply["result"]["score"])
    else:
        print("Intent : ",google_reply["result"]["metadata"]["intentName"]," Score : ", google_reply["result"]["score"])
    ibm_reply= ibm.getPrediction(userInput)
    print("Prediction on Watson Assistant")
    ibm_reply=ibm_reply["intents"]
    if(len(ibm_reply)<1 or ibm_reply==""):
        print("Intent : No User Defined Intent Found ", "Score : 1")
    for i in ibm_reply:
        print("Intent : ",i["intent"], " Score : ", i["confidence"])
    da=td.getPrediction(userInput)
    print(da)
    print("Our Preditcion Method in detial")
    print("Similarity Intent ", da[0]["Intent"], " ,Score :", da[0]["Score"])
    print("Negation Intent ", da[1]["Intent"], " ,Score :", da[1]["Score"])

if __name__ == "__main__":

    #Welcome Program
    print("","-"*100,
          "\n\tWelcome to Demo of *Improving Intent Classifier in Virtual Voice Assistant*\n",
          "-"*100)

    #Reset Module
    print("Reseting All virtual Voice agents")
    #resetApplication();
    print ("Reset Done")
    print ("_"*100)


    #StartProgram
    name = -1
    while(True):
        option = int(input("Choose Option \n1. Show Intents \n2. Create Intent "
                         "\n3. Add Single Phrase in Intent \n4. Add Mutiple Phrase in Intent \n5. Get Predcition "
                         "\n6. Reset Application \n0. to EXIT\n"))

        if(option<1 or option > 6):
            break

        if(option==1):
            getIntentList()

        if(option==2):
            name = str(input("\nName of the Intent: "))
            createIntent(name)

        if(option == 3):
            temp = ibm.getIntentList()
            print("INTENTS PRESENT NOW")
            temp = temp["intents"]
            for intent in temp:
                print(intent["intent"])
            print("-" * 25)
            name = str(input("\nType name of the Intent from above: "))
            text = str(input("\nType training phrase for "+name+ " "))
            add_utterance(text,name)
            time.sleep(10)

        if(option == 4):
            temp = ibm.getIntentList()
            print("INTENTS PRESENT NOW")
            temp = temp["intents"]
            for intent in temp:
                print(intent["intent"])
            print("-" * 25)
            name = str(input("\nType name of the Intent from above: "))
            length = int(input("\nEnter no of lines you want to add : "))
            text=[]
            while(len(text)<length):
                inp = str(input("\nEnter " + str(len(text)+1) + " line you want to add : "))
                text.append(inp)
            add_utterances(text,name)
            time.sleep(10)

        if (option == 5):
            userInput = str(input("\nType Test phrase "))
            getPrediction(userInput)

        if(option==6):
            print("Reseting All virtual Voice agents")
            resetApplication();
            time.sleep(10)
            print ("Reset Done")
            print ("_" * 100)













