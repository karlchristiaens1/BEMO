class Twitter:
    def __init__(self, res):
        self.message = ""
        self.dm_person = ""
        self.dm_message = ""
    
    def get_message(self, res):
        # print(res)
        for i in res["syntax"]["tokens"]:
            if i["text"] == "say" or i["text"] == "saying":
                endLocation = i["location"][1]
                # message = response["syntax"]["sentences"][0]["text"].split("")
                message = [i for i in res["syntax"]["sentences"][0]["text"] ]
                messageFiltered = message[endLocation+1:res["syntax"]["sentences"][0]["location"][1]]
                finalMessage = "".join(str(e) for e in messageFiltered)
                return finalMessage
                # print("HERE: ", "".join(str(e) for e in messageFiltered))
            # pass
        return "ERROR_NO_MESSAGE"

    def get_dm_person(res):
        pass

    def get_dm_message(res):
        pass

class News:
    def __init__(self):
        self.message = ""
        self.dm_person = ""
        self.dm_message = ""

class Podcasts:
    def __init__(self):
        self.message = ""
        self.dm_person = ""
        self.dm_message = ""


def sentences_testing():
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


#For Testing Purposes - To be deleted
import API_NLU

possibleActions = [
        "send tweet",
        "read tweet",
        "send direct message",
        "read direct message",
        "read news",
        "play podcast"
    ]

sentencesList = [
'Post a tweet saying i am very angry today',
'Send a tweet saying the weather is warm',
'Tweet that the weather is hot',
'Publish a tweet saying the weather is hot',
'Read my last tweet',
'Read the last tweet I received',
'Read the latest tweet I received',
'Read my newest tweet',
'Read all my tweets',
'Read the last 5 tweets',
'Speak my tweets',
'Tell me my tweets',
'Did I receive any tweets',
'Did I receive any direct messages',
'Can you read my direct message',
'Can you tell me my direct message',
'Reply to this tweet that the weather is hot',
'Respond to the tweet the weather is hot',
'Respond on twitter that the weather is hot',
'Read the latest news',
'Read today\'s news',
'Read this week\'s news',
'Read the news from this journal',
'Read news about oil prices',
'Play a podcast of Joe Rogan',
'Play a podcast on science',
'Play me a random podcast',
'Play me a podcast on art'
]

#TODAY:
#Loop
#Store the message for each sentence
#Correct Algorithm: 1. Sending Direct Message (Look at twitter code, it will need USername of person ect...)
                  # 2. Message for diret message needs to be understood
#Integrate each service
#Clean Code
# Generate more sentences to test algorithm on

#Creating empty Action requestion list:
actionResponses = []
#Creating Empty Specific list:
specificAction = []

print("Started Tests: ")
for i in range(0, len(sentencesList)):
    #Obtaining the response for each sentence
    response = API_NLU.NLU(sentencesList[i])
    # print(response)

    #Obtaining teh action requested for each sentence
    ar = API_NLU.action_request(response) 
    
    #Adding each sentences' action to the list
    actionResponses.append(ar)

    #Instantiating the correct class object & its contents
    if ar == possibleActions[0]:
        print(possibleActions[0])
        X = Twitter(response)
        # X.get_message()
        specificAction.append(X.get_message(response))

    elif ar == possibleActions[1]:
        print(possibleActions[1])
        X = Twitter(response)
        specificAction.append("")

    elif ar == possibleActions[2]:
        print(possibleActions[2])
        X = Twitter(response)
        # X.get_message()
        specificAction.append(X.get_message(response))

    elif ar == possibleActions[3]:
        print(possibleActions[3])
        X = Twitter(response)
        specificAction.append("")

    elif ar == possibleActions[4]:
        print(possibleActions[4])
        X = News()
        specificAction.append("")

    elif ar == possibleActions[5]:
        print(possibleActions[5])
        X = Podcasts()
        specificAction.append("")
    else:
        print('error') #ask user to repeat
        specificAction.append("")
    print("...Sentence " + str(i) + " completed")

import pandas as pd

data = {"Sentences" : sentencesList, 'Action Results' : actionResponses, 'Specific' : specificAction}
df = pd.DataFrame(data)
# print(df)
df.to_excel('OneDrive - University College London/ELEC0036/IBM Project/Code/NLUSentenceAnalysis.xlsx')
