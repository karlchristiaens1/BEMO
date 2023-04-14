import xml.sax
import BEMO_secrets as secrets

bemo_path = '/home/pi/Desktop/BEMO/BEMO-main/'
#DOWNLOADING AUDIO FROM HTTP LINK INTO A FILE
def convert_link_to_file(url):
    import requests

    # url = 'https://play.podtrac.com/npr-510366/edge1.pod.npr.org/anon.npr-mp3/npr/ukraine/2023/01/20230127_ukraine_38e592f0-1ca4-4239-83b5-f4d381c1fd8f.mp3?awCollectionId=510366&awEpisodeId=1152132316&orgId=1&d=257&p=510366&story=1152132316&t=podcast&e=1152132316&size=4096880&ft=pod&f=510366'
    response = requests.get(url)

    with open(bemo_path+'podcast.mp3', 'wb') as f:
        f.write(response.content)

#API CALL TO LISTEN NOTES        
def call_listen_notes(keyword): #Takes a user keyword, returns a list of matching podcasts
    import json
    from listennotes import podcast_api

    client = podcast_api.Client(api_key=secrets.LISTEN_NOTES_APIKEY)
    response = client.search(q=keyword,).json()["results"]
    
    # print(json.dumps(response, indent = 2))
    # Initialising empty url & titles dict format & a url data list
    
    url_data_list = []
    
    for i in range(0,3):
        url_dict = {
            "url" : "",
            "title" : ""
        }
        url_dict["url"] = (response[i]['audio'])
        url_dict["title"] = (response[i]['title_original'])
        url_data_list.append(url_dict)

    print(json.dumps(url_data_list, indent = 2))

    return url_data_list

#Cleaning and preparing data for text-to-speech service
def tts_data_prep(data):
    podcast_numbers = ['first', 'second', 'third', 'fourth', 'fifth']
    speach_string = ""
    if len(data) < 5:
        for i in range(0,len(data)):
            # news_data['articles']['source']['Name']
            speach_string = speach_string + "\nThe " + podcast_numbers[i] + " one is titled: " + data[i]['title'] + "."
        return speach_string
    else:
        for i in range(0,5):
            # news_data['articles']['source']['Name']
            speach_string = speach_string + "\nThe " + podcast_numbers[i] + " one is titled: " + data[i]['title'] + "."
        return speach_string


# For Testing Purposes:
#call_listen_notes('star wars')
# print(tts_data_prep(call_listen_notes('rubies')))
