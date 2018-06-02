import requests,base64,sys, os.path, json, time,copy

headers=\
{
    'Authorization':'Bearer 23680a24223848129ff736e4fcb272d2',
    'Content-Type':'application/json'
}
IntentList={}

def getIntentList():
    try:
        conn = requests.get("https://api.dialogflow.com/v1/intents?v=20150910",data={},headers=headers)
        data=conn.content
        data=json.loads(data.decode("utf-8"))
        for intents in data:
            IntentList[intents["name"]]=intents["id"]
        return IntentList
    except Exception as e:
        print("THESIS NEGATION GET INTENT LIST: [Errno {0}]".format(e))



def createIntent(name):
    body = {"name": name }
    try:
        conn = requests.post("https://api.dialogflow.com/v1/intents?v=20150910",data = json.dumps(body), headers = headers)
        print("THESIS NEGATION CREATED INTENT:",name)
    except Exception as e:
        print("THESIS NEGATION CREATE INTENT:[Errno {0}]".format(e))

def deleteIntent(id):
    try:
        url="https://api.dialogflow.com/v1/intents/"+str(id) +"?v=20150910"
        conn = requests.delete(url,data = {}, headers = headers)
        print("THESIS NEGATION DELETED INTENT:",conn.status_code,conn.reason)
    except Exception as e:
        print("THESIS NEGATION DELETED INTENT:[Errno {0}]".format(e))

def resetApplication():
    IntentList=getIntentList()
    for key in IntentList:
        if(key == "Default Fallback Intent"):
            continue
        if (key == "Default Welcome Intent"):
            continue;
        print("THESIS NEGATION RESET IS DELETING INTENT:",key)
        deleteIntent(IntentList[key])
    print("THESIS NEGATION RESET DONE")


def getPrediction(query):
    body = \
        {
            "lang": "en",
            "query": query,
            "sessionId": "temp"
        }
    try:
        conn = requests.post("https://api.dialogflow.com/v1/query?v=20150910",data = json.dumps(body), headers = headers)
        data=conn.content
        data=json.loads(data.decode("utf-8"))
        return data
    except Exception as e:
        print("[Errno {0}]".format(e))

def add_utterance(input,intent):
    IntentList = getIntentList()
    Usersays=[]
    userSay={
            "count": 0,
            "data" :
            [
                {
                    "text" : " "
                }
            ]
    }
    data=getIntent(IntentList[intent])
    data=data["userSays"]
    for say in data:
        userSay["data"][0]["text"]=say["data"][0]["text"]
        Usersays.append(copy.deepcopy(userSay))



    userSay["data"][0]["text"] = input
    Usersays.append(copy.deepcopy(userSay))

    body=\
    {
        "name":intent,
        "userSays":Usersays
    }
    try:
        url="https://api.dialogflow.com/v1/intents/"+ IntentList[intent]+"?v=20150910"
        conn = requests.put(url,data = json.dumps(body), headers = headers)
        print ("THESIS NEGATION ADDED DATA IN INTENT " + intent)
    except Exception as e:
        print("THESIS NEGATION [Errno {0}]".format(e))



def getIntent(id):
    try:
        url="https://api.dialogflow.com/v1/intents/"+id +"?v=20150910"
        conn = requests.get(url,data = {}, headers = headers)
        return json.loads(conn.content.decode("utf-8"))
    except Exception as e:
        print("THESIS NEGATION [Errno {0}]".format(e))


def add_utterances(input,intent):
    IntentList = getIntentList()
    Usersays = []
    userSay = {
        "count": 0,
        "data":
            [
                {
                    "text": " "
                }
            ]
    }
    data = getIntent(IntentList[intent])
    data = data["userSays"]
    for say in data:
        userSay["data"][0]["text"] = say["data"][0]["text"]
        Usersays.append(copy.deepcopy(userSay))

    for say in input:
        userSay["data"][0]["text"] = say
        Usersays.append(copy.deepcopy(userSay))

    body = \
        {
            "name": intent,
            "userSays": Usersays
        }
    try:
        url = "https://api.dialogflow.com/v1/intents/" + IntentList[intent] + "?v=20150910"
        conn = requests.put(url, data=json.dumps(body), headers=headers)
        print ("THESIS NEGATION ADDED DATA IN INTENT " + intent)
    except Exception as e:
        print("THESIS NEGATION [Errno {0}]".format(e))
