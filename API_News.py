import json
import BEMO_secrets as secrets

def get_time_today():
    # importing datetime module
    import datetime
    # using today() to get current date
    Current_Date_Formatted = datetime.datetime.today().strftime ('%Y-%m-%d') # format the date to ddmmyyyy
    # print ('Current Date: ' + str(Current_Date_Formatted))    
    return Current_Date_Formatted

def get_time_last_month():  #Time 21 days ago to be accurate
    # importing datetime module
    import datetime
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=21)
    Previous_Date_Formatted = Previous_Date.strftime ('%Y-%m-%d') # format the date to ddmmyyyy
    # print ('Previous Date: ' + str(Previous_Date_Formatted))
    return Previous_Date_Formatted

# def get_categories():
#     #All Catergories:
#     categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
#     return categories

def news_call():
    from newsapi import NewsApiClient
    # Initialising  
    newsapi = NewsApiClient(api_key=secrets.NEWS_API_APIKEY)
    
    #Calling API with pre-defined sources
    all_articles = newsapi.get_everything(q='',
                                          sources='bbc-news,the-verge',
                                          domains='bbc.co.uk,techcrunch.com',
                                          from_param=  get_time_last_month(),
                                          to= get_time_today(),
                                          language='en',
                                          sort_by='relevancy',
                                          page=2)

    # sources = newsapi.get_sources()
    return all_articles


# FOR TESTING PURPOSES
#print(json.dumps(news_call(""), indent = 2))
# print(get_time_today())
# print(get_time_last_month())

def tts_data_prep(): # Preparing daily news for the text-to-speech service 
    news_data = news_call("")
    speach_string = ""
    for i in range(0,3):
        # news_data['articles']['source']['Name']
        speach_string = speach_string + "From " + news_data['articles'][i]['source']['Name'] + ". " + news_data['articles'][i]['title'] + ".\n"
    return speach_string



