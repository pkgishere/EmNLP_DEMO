import requests
import random
apiUrl = 'https://api.dialogflow.com/v1/query?v=20150910'

headers = {
	"Authorization":"Bearer 9fcf861bf3af42e6a53c04ef9fdf197a",
	"Content-Type":"application/json"
}
def postQuery(text):
	payload = {
		"lang": "en",
		"query":text,
		"sessionId": "12345"
	}
	r = requests.post(apiUrl,data=payload)
	print(r.status_code)

def postIntent(name):
	intent = {
		"name": name,
		"displayName": name,
		"mlEnabled": True,
		"trainingPhrases": [

			{
				"name": "test intent 5",
				"type": "EXAMPLE",
				"parts": [
					{
						"text": "5",
						"entityType": "@sys.number",
						"alias": "number",
						"userDefined": False,
					}
				],
				"timesAddedCount": 5,
			}

		],
		"resetContexts": False,
	}

	r = requests.post(apiUrl,data=intent)
	print(r)

postIntent("Testing")


