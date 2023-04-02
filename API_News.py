import json
import BEMO_secrets as secrets

def get_time_today():
    # importing datetime module
    import datetime
    # using today() to get current date
    Current_Date_Formatted = datetime.datetime.today().strftime ('%Y-%m-%d') # format the date to ddmmyyyy
    # print ('Current Date: ' + str(Current_Date_Formatted))    
    return Current_Date_Formatted

def get_time_last_month():
    # importing datetime module
    import datetime
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=21)
    Previous_Date_Formatted = Previous_Date.strftime ('%Y-%m-%d') # format the date to ddmmyyyy
    # print ('Previous Date: ' + str(Previous_Date_Formatted))
    return Previous_Date_Formatted

def get_categories():
    #All Catergories:
    categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    return categories

def news_call(category_of_interest):
    # API_KEY = 'fe989672aff3498fa906c1538da30214'

    from newsapi import NewsApiClient

    # Init
    newsapi = NewsApiClient(api_key=secrets.NEWS_API_APIKEY)
    
    # /v2/top-headlines
    # top_headlines = newsapi.get_top_headlines(q=category_of_interest,
    #                                         # sources='bbc-news,the-verge',
    #                                         # category=category_of_interest,
    #                                         language='en')
    #                                         # country='us, uk')

    # # /v2/everything

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

#Receive Subject
#Predefine Sources
#Can be altered
#Date by default 1 month period
#I need to get the current date, & look 1 month back
# I can create an extra parameter for the amount of different news i want to display
#For paramter there is a default (except q = "" empty)

#In the main program, after speech to text, 
# if news API is called, 
# Update those parameters
# Call parameters
# Render Results

#print(json.dumps(news_call(""), indent = 2))
# print(get_time_today())
# print(get_time_last_month())

def tts_data_prep():
    news_data = news_call("")
    speach_string = ""
    for i in range(0,3):
        # news_data['articles']['source']['Name']
        speach_string = speach_string + "From " + news_data['articles'][i]['source']['Name'] + ". " + news_data['articles'][i]['title'] + ".\n"
    return speach_string



