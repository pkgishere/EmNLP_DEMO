import http.client, urllib.request, urllib.parse, urllib.error, base64,sys, os.path, json, time, requests, copy

headers = \
{
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'ef848db7c6d44659a478b36cf5449e29',
}

def getPrediction(text):
    params =\
    {
        'q': text,
    }
    try:
        r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/4a2d8c53-7be9-440a-961b-fbfc3e75fffe',headers=headers, params=params)
        return r.json()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def createIntent(name):
    body = '{"name":'+ '"'+str(name)+'" }'
    params = urllib.parse.urlencode({})
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/luis/api/v2.0/apps/4a2d8c53-7be9-440a-961b-fbfc3e75fffe/versions/0.1/intents?%s", body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        train()
        print ("MICROSOFT LUIS CREATED INTENT ", name)
        return data
    except Exception as e:
        print("[Errno {0}]".format(e))

def getIntentList():
    params = urllib.parse.urlencode({})
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("GET", "/luis/api/v2.0/apps/4a2d8c53-7be9-440a-961b-fbfc3e75fffe/versions/0.1/intents?%s", "", headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}]".format(e))


def resetApplication():
    data = getIntentList()
    for i in data:
        if(i["name"]=="None"):
            continue
        else:
            deleteIntent(i["id"])
    publish()
    print("MICROSOFT LUIS RESET DONE")

def deleteIntent(IntentId):
    params = urllib.parse.urlencode({})
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        if(type(IntentId)!=type("a")):
            IntentId=IntentId.decode("utf-8").replace('"', '')
        conn.request("DELETE", "/luis/api/v2.0/apps/4a2d8c53-7be9-440a-961b-fbfc3e75fffe/versions/0.1/intents/"+IntentId+"?%s", "{body}",
                     headers)
        response = conn.getresponse()
        data = response.read()
        publish()
        conn.close()
        print("MICROSOFT LUIS DELETED INTENT")
        return data
    except Exception as e:
        print("[Errno {0}]".format(e))

# Authoring key, available in luis.ai under Account Settings
LUIS_authoringKey = "ef848db7c6d44659a478b36cf5449e29"

# ID of your LUIS app to which you want to add an utterance
LUIS_APP_ID = "4a2d8c53-7be9-440a-961b-fbfc3e75fffe"

# The version number of your LUIS app
LUIS_APP_VERSION = "0.1"

# Update the host if your LUIS subscription is not in the West US region
LUIS_HOST = "westus.api.cognitive.microsoft.com"

# uploadFile is the file containing JSON for utterance(s) to add to the LUIS app.
# The contents of the file must be in this format described at: https://aka.ms/add-utterance-json-format
UTTERANCE_FILE = "./utterances.json"
RESULTS_FILE = "./utterances.results.json"



class LUISClient:
    # endpoint method names
    TRAIN = "train"
    EXAMPLES = "examples"

    # HTTP verbs
    GET = "GET"
    POST = "POST"

    # Encoding
    UTF8 = "UTF8"

    # path template for LUIS endpoint URIs
    PATH = "/luis/api/v2.0/apps/4a2d8c53-7be9-440a-961b-fbfc3e75fffe/versions/0.1/"

    # default HTTP status information for when we haven't yet done a request
    http_status = 200
    reason = ""
    result = ""

    def __init__(self, host, app_id, app_version, key):
        if len(key) != 32:
            raise ValueError("LUIS subscription key not specified in " +
                             os.path.basename(__file__))
        if len(app_id) != 36:
            raise ValueError("LUIS application ID not specified in " +
                             os.path.basename(__file__))
        self.key = key
        self.host = host
        self.path = self.PATH.format(app_id=app_id, app_version=app_version)

    def call(self, luis_endpoint, method, data=""):
        path = self.path + luis_endpoint
        headers = {'Ocp-Apim-Subscription-Key': self.key}
        conn = http.client.HTTPSConnection(self.host)
        conn.request(method, path, data.encode(self.UTF8) or None, headers)
        response = conn.getresponse()
        self.result = json.dumps(json.loads(response.read().decode(self.UTF8)),
                                 indent=2)
        self.http_status = response.status
        self.reason = response.reason
        return self

    def add_utterance(self, text,intent):
        data=[{
                "text": text,
                "intentName": intent,
                "entityLabels": []
             }]

        data=str(data)
        self.train()
        self.call(self.EXAMPLES, self.POST, data)
        print ("MICROSOFT LUIS ADDED DATA IN INTENT "+ intent)

    def add_utterances(self, List,intent):
        temp={
                "text": "",
                "intentName": intent,
                "entityLabels": []
             }
        data=[]
        for i in List:
            temp["text"]=i;
            data.append(copy.deepcopy(temp))
        data=str(data)
        print ("MICROSOFT LUIS ADDED DATA IN INTENT " + intent)
        self.train()
        self.call(self.EXAMPLES, self.POST, data)

    def train(self):
        self.call(self.TRAIN, self.GET)
        return self.call(self.TRAIN, self.POST)

    def status(self):
        return self.call(self.TRAIN, self.GET)

    def write(self, filename=RESULTS_FILE):
        if self.result:
            with open(filename, "w", encoding=self.UTF8) as outfile:
                outfile.write(self.result)
        return self

    def print1(self):
        if self.result:
            print(self.result)
        return self

    def raise_for_status(self):
        if 200 <= self.http_status < 300:
            return self
        raise http.client.HTTPException("{} {}".format(
            self.http_status, self.reason))

luis = LUISClient(LUIS_HOST, LUIS_APP_ID, LUIS_APP_VERSION,
                      LUIS_authoringKey)


def publish():
    body = '{"versionId": "0.1","region": "westus"}'
    params = urllib.parse.urlencode({
    })

    try:
        train()
        time.sleep(5)
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/luis/api/v2.0/apps/4a2d8c53-7be9-440a-961b-fbfc3e75fffe/publish?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print("MICRSOFT LUIS PUBLISH")
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def train():
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/luis/api/v2.0/apps/4a2d8c53-7be9-440a-961b-fbfc3e75fffe/versions/0.1/train?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))




