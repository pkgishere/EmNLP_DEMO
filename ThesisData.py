import nltk
from nltk.corpus import wordnet
import itertools
import DialogFlowIntent_2 as df
import DialogFlowIntent_3 as df2
import random

def createSimilarSentences(line):
    text = nltk.word_tokenize(line)
    list = nltk.pos_tag(text)
    adj = []
    modal=[]
    noun=[]
    adverb=[]
    particle=[]
    verb=[]

    longList=[]
    longListNeg=[]
    postion=set()
    count =0
    for i in list:
        if (i[1].startswith("JJ")):
            postion.add(count)
            adj.append(i[0])
            longList.append(getSimilarWords(i[0]))
            longListNeg.append(i[0])
        elif (i[1].startswith("MD")):
            postion.add(count)
            modal.append(i[0])
            longList.append(getSimilarWords(i[0]));
            longListNeg.append(i[0])

        elif (i[1].startswith("RB")):
            postion.add(count)
            adverb.append(i[0])
            longList.append(getSimilarWords(i[0]));
            longListNeg.append(i[0])

        elif (i[1].startswith("RP")):
            postion.add(count)
            particle.append(i[0])
            longList.append(getSimilarWords(i[0]))
            longListNeg.append(i[0])


        # elif (i[1].startswith("NN") and (not (i[1].startswith("NNP")))):
        #     postion.add(count)
        #     noun.append(i[0])
        #     longList.append(getSimilarWords(i[0]))
        #     longListNeg.append(i[0])


        elif (i[1].startswith("VB")):
            postion.add(count)
            verb.append(i[0])
            longList.append(getSimilarWords(i[0]))
            if (count > 0 and not (str(list[count - 1]).startswith("no"))):

                a=getNonSimilarWords(i[0])
                a.add("not " + str(i[0]))
                if(str(i[0]) in a):
                    a.remove(str(i[0]))
                longListNeg.append(a)
            else:
                a = getNonSimilarWords(i[0])
                if (str(i[0]) in a):
                    a.remove(str(i[0]))
                longListNeg.append(a)

        else:
            longList.append(i[0]);
            longListNeg.append(i[0])

        count+=1

    # print(adverb,adj,modal,noun,particle,verb)
    # print(postion)
    # print(longList)
    # print(longListNeg)

    Negsentence=[]
    counter_verb_global=1
    loop=len(verb)
    finalList=[]
    if(len(verb)>1):
        while(loop>0):
            loop=loop-1
            counter_verb_Inside = 1;
            count=-1
            for i in list:
                count+=1
                if(i[1].startswith("VB") and counter_verb_Inside == counter_verb_global):
                    counter_verb_Inside+=1
                    Negsentence.append(longListNeg[count])
                else:
                    if (i[1].startswith("VB")):
                        counter_verb_Inside += 1
                    Negsentence.append(i[0])
            counter_verb_global+=1
            finalList=finalList+generateSentence(Negsentence)
            Negsentence=[]
        return(generateSentence(longList),finalList)
    else:
        return(generateSentence(longList),generateSentence(longListNeg))


def generateSentence(li):
    c=li[0]
    for i in range(1,len(li)):
        a=c
        if(type(li[i])==type("a")):
            b=[li[i]]
        else:
            b=list(li[i])
        c=[name1+" "+name2 for name1 in a for name2 in b]
    return c

def getSimilarWords(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name().replace("_"," "))
    if(len(synonyms)<1):
        synonyms=[word]
    return set(synonyms)

def getNonSimilarWords(word):
    antonyms=[]
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name().replace("_"," "))
    if (len(antonyms) < 1):
        antonyms = [word]
    return set(antonyms)

def createIntent(name):
    df.createIntent(name+"_sim")
    df2.createIntent(name+"_neg")

def add_utterance(text,intent):
    sim,diff= createSimilarSentences(text)
    temp=[]
    if (len(sim) > 200):
        a=random.sample(range(0,len(sim)),200)
        for i in a:
            temp=temp+[sim[i]]
        sim=temp
    temp=[]
    if (len(diff) > 200):
        a=random.sample(range(0,len(diff)),200)
        for i in a:
            temp=temp+[diff[i]]
        diff=temp
    sim=sim+[text]
    df.add_utterances(sim,intent+"_sim")
    df2.add_utterances(diff, intent + "_neg")

def resetApplication():
    df.resetApplication()
    df2.resetApplication()

def add_utterances(li, intent):
    sim=[]
    diff=[]
    for i in li:
        si, di = createSimilarSentences(i)
        sim=sim+si
        diff=diff+di
    temp=[]
    if (len(sim) > 180):
        a = random.sample(range(0, len(sim)), 180)
        for i in a:
            temp = temp + [sim[i]]
        sim = temp
    temp = []
    if (len(diff) > 200):
        a = random.sample(range(0, len(diff)), 200)
        for i in a:
            temp = temp + [diff[i]]
        diff = temp
    sim=sim+li
    df.add_utterances(sim, intent + "_sim")
    df2.add_utterances(diff, intent + "_neg")

def getPrediction(text):
    data_sim=df.getPrediction(text)
    data_diff=df2.getPrediction(text)
    # print(data_diff,data_sim)
    di={"Intent": str(data_diff["result"]["metadata"]["intentName"])[:-4], "Score": data_diff["result"]["score"]}
    si={"Intent": str(data_sim["result"]["metadata"]["intentName"])[:-3], "Score": data_sim["result"]["score"]}
    return si,di

def showIntent():
    print(df.getIntentList())
    print(df2.getIntentList())







