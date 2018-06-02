import json
import watson_developer_cloud, copy
from time import gmtime, strftime


assistant = watson_developer_cloud.AssistantV1\
(
        username="04f281dd-5038-4b53-a6ab-533cc717544f",
        password="jo8vla8Otw2H",
        version="2018-02-16"
)
#workSpaceID
w_id = 'dc846ce4-56c9-408f-a37c-9aef0a7daf91'

def createIntent(name):
    response = assistant.create_intent\
            (
                workspace_id = w_id,
                intent = name
            )
    print("WATSON ASSISTANT CREATED INTENT ", name)

def getIntentList():
    response = assistant.list_intents\
            (
                workspace_id=w_id
            )
    return response
def getIntent(name):
    response = assistant.get_intent\
        (
            workspace_id = w_id,
            intent = name
        )
    return response

def add_utterance(text,intent):
    response = assistant.update_intent\
            (
                workspace_id=w_id,
                intent=intent,
                new_examples=[
                                {'text': text}
                            ],
                new_description='Updated intent on' + str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            )
    print("WATSON ASSISTANT ADDED UTTERANCE IN INTENT ", intent)

def deleteIntent(name):
    response = assistant.delete_intent\
        (
            workspace_id = w_id,
            intent = name
        )
    print("WATSON ASSISTANT DELETED INTENT ", name)


def add_utterances(input,intent):
    phrases = []
    example = {"text": ""}
    for text in input:
        example["text"]=text
        phrases.append(copy.deepcopy(example))
    response = assistant.update_intent \
        (
            workspace_id=w_id,
            intent=intent,
            new_examples=phrases,
            new_description='Updated intent on' + str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        )
    print("WATSON ASSISTANT ADDED UTTERANCES IN INTENT ", intent)

def resetApplication():
    intentList = getIntentList()
    intentList=intentList["intents"]
    for intentObject in intentList:
        deleteIntent(intentObject["intent"])
    print("WATSON ASSISTANT RESET DONE")

def getPrediction(userInput):
    response = assistant.message\
            (
                workspace_id=w_id,
                input={
                            'text': userInput
                      }
            )
    return response
