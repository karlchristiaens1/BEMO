import BEMO_secrets as secrets
def NLU(sentence):
    import json
    import pandas as pd 
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson.natural_language_understanding_v1  import Features, EntitiesOptions, KeywordsOptions, EmotionOptions, SemanticRolesOptions, SyntaxOptions, SyntaxOptionsTokens, ConceptsOptions
    import Database_Cloudant as dbc
    # API_KEY = "6UV4rJoH0dFoqjUErdw1IjZ3p_iC2Zy6DUVY8R6BGoV5"

    authenticator = IAMAuthenticator(secrets.IBM_NLU_APIKEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)
    # URL_SERVICE = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com"
    URL_SERVICE="https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/86decc3e-8683-4706-aa33-f64035a2f6d4"

    natural_language_understanding.set_service_url(URL_SERVICE)
    response = natural_language_understanding.analyze(
        text = sentence,
        features=Features(
            emotion=EmotionOptions(),
            semantic_roles=SemanticRolesOptions(),
            syntax=SyntaxOptions(sentences=True, tokens=SyntaxOptionsTokens(lemma=False,part_of_speech=True)),
            entities=EntitiesOptions(emotion=False, sentiment=False, limit=5),
            keywords=KeywordsOptions(emotion=False, sentiment=False,
                                    limit=2),
            concepts=ConceptsOptions(limit = 3)),
        language = "en"
                                    ).get_result()
    
    # print("Here 1")
    #Always Call Continous Monitoring when calling NLU
    # dbc.create_cm_doc([emotion_score(NLU(sentence))])
    # print("Here 2")
    # Displaying Results Directly 
    # print(json.dumps(response, indent=2))
    return response


#############
#  Keywords
#############
def keywordTwitter(res): #finding Twitter related  keywords
    for i in res["keywords"]:
        # print(i)
        x = i["text"].lower()
        accepted_strings = {'twitter', 'tweet', 'tweets', 'latest tweet','newest tweet',
                            'new tweet', 'new tweets',
                            'last tweet', 'last tweets', 'latest tweets', 
                            'dm', 'dms', 'direct messages', 'direct message'}
        if x in accepted_strings:

            return True
    # print("Executed Here")
    return False

def keywordDM(res): #finding direct messages related keywords
    for i in res["keywords"]:
        # print(i)
        accepted_strings = {'dm', 'dms', 'direct messages', 'direct message'}
        if i['text'] in accepted_strings:
            return True
        # if i["text"] == "direct message" or i["text"] == "direct messages" or i["text"].lower() == "dms" or i["text"].lower() == "dm":
        #     # print("true!") 
        #     return True
    return False

def keywordNews(res): #Finding news-related keywords
    for i in res["keywords"]:
        # print(i)
        x = i["text"].lower()
        accepted_strings = {'news', 'events', 'latest news', 'latest events', 'newest news', 'newest events',
                            'new news', 'new events','last news', 'last events', 'today\'s news', 'week\'s news'
                            }
        if x in accepted_strings:
            return True
    return False

def keywordPodcasts(res): #Fidning podcast re-lated keywords
    accepted_strings = {'podcasts', 'podcast', 'podcasting', 'random podcast', 'newest podcast', 'latest podcast'} 
    for i in res["keywords"]:
        # print(i)
        x = i["text"].lower()
        if x in accepted_strings:
            return True
    for i in res["concepts"]:
        # print(i)
        x =  i['text'].lower()
        if x in accepted_strings:
            return True
    # print("Executed Here")
    return False


#################
#    ACTIONS
#################
def actionSend(res):
    accepted_strings = {'send', 'text', 'publish', 'post'}

    try:
    #SEMANTIC ANALYSIS
        x = res["semantic_roles"][0]["action"]["verb"]["text"]
        #PERFORM AN ERROR CHECK HERE
        # print(x, "ERROR-SEND-SEMANTIC")
        if x.lower() in accepted_strings:
            return True
        else:
            raise ValueError     
    except(IndexError, ValueError):
        #SYNTAX ANALYSIS
        # print(response["syntax"]["tokens"])
        for i in res["syntax"]["tokens"]:
            # print(i)
            if i['text'].lower() in accepted_strings:
                return True
    return False

def actionRead(res):#Works for Single command sentence!
    accepted_strings = {'read', 'receive', 'tell', 'recite', 'speak'}
    try:
        # SEMANTIC ANLALYSIS
        # print(response["semantic_roles"][0]["action"]["verb"]["text"].lower())
        x = res["semantic_roles"][0]["action"]["verb"]["text"].lower()
        if x in accepted_strings:
            return True
    except(IndexError):
        #SYNTAX ANALYSIS
        for i in res["syntax"]["tokens"]:
            # print(i)
            if i["text"].lower() in accepted_strings:
                return True

def actionPlay(res):#Works for Single command sentence!
    # print('here')
    accepted_strings = {'start', 'play', 'tell', 'recite', 'speak'}
    try:
        # SEMANTIC ANLALYSIS
        # print(response["semantic_roles"][0]["action"]["verb"]["text"].lower())
        x = res["semantic_roles"][0]["action"]["verb"]["text"].lower()
        if x in accepted_strings:
            return True
        else:
            raise IndexError
    except(IndexError):
        #SYNTAX ANALYSIS
        for i in res["syntax"]["tokens"]:
            # print(i)
            if i["text"].lower() in accepted_strings:
                return True

def actionReply(res):
    accepted_strings = {'reply', 'respond'}
    try:
        # SEMANTIC ANALYSIS
        # print(response["semantic_roles"][0]["action"]["verb"]["text"])
        x = res["semantic_roles"][0]["action"]["verb"]["text"].lower()
        if x in accepted_strings:
            return True
        else:
            raise IndexError
    except(IndexError):
        #SYNTAX ANALYSIS
        # print(response["syntax"]['tokens'])
        for i in res["syntax"]['tokens']:
            if i['text'].lower() in accepted_strings:
                return True

    return False


def emotion_score(res):
    emo_score = res['emotion']['document']['emotion']
    return emo_score

possibleActions = [
    "send tweet",
    "read tweet",
    "send direct message",
    "read direct message",
    "read news",
    "play podcast"
]

######################
#    SUBSYSTEM CALL
######################
def action_request(res):
    if keywordTwitter(res):
        if actionSend(res):
            if keywordDM(res):
                return (possibleActions[2])
            else:
                return (possibleActions[0])
            # print("Message:", messageConveyed())
        elif actionRead(res):
            if keywordDM(res):
                return(possibleActions[3])
            return (possibleActions[1])
        elif actionReply(res):
            return ("reply tweet")  
        else:
            return ("Error 1")
    elif keywordNews(res):
        if actionRead(res):
            return (possibleActions[4])
            #To be completed for further actions & keywords
        else:
            return ("Error 2")
    elif keywordPodcasts(res):
        if actionPlay(res):
            return (possibleActions[5])
            #To be completed for further actions & keywords
        else:
            return ("Error 3")
    else:
        return ('.... I do not recognise this command. Please, try again!')



# return  action_chosen(NLU(sentence))

    # {'sadness': 0.031585, 'joy': 0.027666, 'fear': 0.014837, 'disgust': 0.022785, 'anger': 0.907784}

# NLU('Post a tweet saying i am very angry today')

def sentences_testing(sentencesList):
    import pandas as pd
    actionResponses = [] #Setting up empty list
    # print(CHANGE(sentencesList[0]))
    print("Started Tests: ")
    for i in range(0, len(sentencesList)):
        # append(i)
        # print(NLU(sentencesList[i]))
        actionResponses.append(action_request(NLU(sentencesList[i])))
        print("...Sentence " + str(i) + " completed")
        pass
    data = {"Sentences" : sentencesList, 'Action Results' : actionResponses}
    df = pd.DataFrame(data)
    # print(df)
    df.to_excel('OneDrive - University College London/ELEC0036/IBM Project/Code/NLUSentenceAnalysis.xlsx')


# sentences_testing()
