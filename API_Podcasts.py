import xml.sax
import secrets

def convert_link_to_file(url):
    import requests

    # url = 'https://play.podtrac.com/npr-510366/edge1.pod.npr.org/anon.npr-mp3/npr/ukraine/2023/01/20230127_ukraine_38e592f0-1ca4-4239-83b5-f4d381c1fd8f.mp3?awCollectionId=510366&awEpisodeId=1152132316&orgId=1&d=257&p=510366&story=1152132316&t=podcast&e=1152132316&size=4096880&ft=pod&f=510366'
    response = requests.get(url)

    with open('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3', 'wb') as f:
        f.write(response.content)

# class Podcasts (xml.sax.ContentHandler):
#     def __init__(self):
#         self.podcast_title = ""
#         self_podcast_link = ""

#     def startElement(self, tag, attributes):
#       self.CurrentData = tag
#       if tag == "college":
#               print("___________________Student Details_____________________")
#               branch = attributes["branch"]
#               print("Branch=", branch)
   
#     def endElement(self, tag):
#         if self.CurrentData == "name":
#             print("Name=", self.name)
#         elif self.CurrentData == "rollno":
#             print("Roll Number=", self.rollno)
#         elif self.CurrentData == "address":
#             print("Address=", self.address)
#         self.CurrentData = ""
    
#     def characters(self, content):
#         if self.CurrentData == "name":
#             self.name = content
#         elif self.CurrentData == "rollno":
#             self.rollno = content
#         elif self.CurrentData == "address":
#             self.address = content
            
# def get_podcast_from_XML():
#     parser = xml.sax.make_parser()
#     parser.setFeature(xml.sax.handler.feature_namespaces, 0)
#     #Object of Students class.
#     X= Podcasts()
#     parser.setContentHandler(X)
#     parser.parse("OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.xml")
    # print()


# get_podcast_from_XML()

def get_podcast_XML():
    import xml.etree.ElementTree as ET

    tree = ET.parse("OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.xml")
    root = tree.getroot()

    # Selecting First rss> channel> item > enclosure tag and url attribute
    root.find(".//rss")

    # Initialising empty url list
    url_list = []

    # Finding entire list of podcasts url and appending them to url_list
    element_list = root.findall(".//channel//item//enclosure")
    for i in range(0,len(element_list)):
        url_list.append(element_list[i].attrib['url'])
    
    #Uncomment to print entire url list
    # print(url_list)
    # url = root.find(".//channel//item//enclosure").attrib['url']

    return url_list[3]

# get_podcast_XML()
# convert_link_to_file(get_podcast_XML())


def call_listen_notes(keyword): #Takes a user keyword, returns a list of matching podcasts
    import json
    from listennotes import podcast_api 
    # 'https://listen-api.listennotes.com/api/v2/best_podcasts'
    # api_key = '6bbf591134cf4c7b82e66f9ca08d476c'

    client = podcast_api.Client(api_key=secrets.LISTEN_NOTES_APIKEY)
    response = client.search(q=keyword,).json()["results"]
    
    # print(json.dumps(response, indent = 2))
    # Initialising empty url & titles dict format & a url data list
    

    url_data_list = []
    
    for i in range(0,len(response)):
        url_dict = {
            "url" : "",
            "title" : ""
        }
        url_dict["url"] = (response[i]['audio'])
        url_dict["title"] = (response[i]['title_original'])
        url_data_list.append(url_dict)

    print(json.dumps(url_data_list, indent = 2))

    return url_data_list

def tts_data_prep(data):
    podcast_numbers = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eight', 'nineth', 'tenth']
    speach_string = ""
    for i in range(0,len(data)):
        # news_data['articles']['source']['Name']
        speach_string = speach_string + "\nThe " + podcast_numbers[i] + " one is titled: " + data[i]['title'] + "."
    return speach_string


# For Testing Purposes:
# call_listen_notes('star wars')
# print(tts_data_prep(call_listen_notes('rubies')))






#Process
# I need to pass in user preference
#User needs to select a podcast from the list.  -> I need pretty print first so user can choose
#Record
# Listen Notes API call -> response
# From Response -> RSS file
#From RSS file -> enclose url -
#Dowload file from url

#NOW I need to figure out how to get 