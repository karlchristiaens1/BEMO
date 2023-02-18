#API KEY: TkYUNN2zGHzR7dy9FPiK37EXj
#API KEY Secret: jzGiqlAtTwBt20Vv3rN4JFKXoJAdKtxIKjPaunsJ0B3RLdlLDG
#Bearer Token AAAAAAAAAAAAAAAAAAAAAHqQgwEAAAAAzkaJ%2BC7vjtgJsUQAJJIFJmPkEoE%3DC57szw9XXVJyJIGTOC90jYJYrvGoSgMwUG0j6yR6JjqkApkqOn
#Access Token: 926587391456006145-uZlPxcg5gfkcmcKP4nMQ53alh89svaj
#Access Token Secret: rzZGxD2mEsrrpksP7VJOUGtwideVt3cjzBRXDlzjGujk8
#
#AUTH2
#Client ID: MVd1SThWMjRMOTZSaGJ1VEN0d2c6MTpjaQ
#Client Secret: 

#Bearer Token 2: emItODMwbWdhZWtvQkFxT0NGb09VbEQwM3kxZDZEV2xBRk1LNWk3WEoxNEZKOjE2NjMwODE3NDIyMzM6MToxOmF0OjE
#Aipetproject2022!
#Bearer Token 3: MGdFLU5YYzVCSm16ZEFKVTktWEdlVllBN3NCQllPR1o4cXNiOF82QTN0Tlk1OjE2NjMwODM0Mzc3OTg6MTowOmF0OjE

#TWITTER MyAIPet
# APIKEY = "rDGY7Bj1nFPVYujn0WNN74UDo"
# APIKEY_SECRET = "J5AdsPzBZ7RtyZvuZECbMWynE0pkn2bBNYoJMLhcFyUYk31GkQ"
# BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAI5%2BhwEAAAAABD%2FTtrDXCiIJ5%2B%2BYI7TDipgRRLg%3DQ9E2KAvOseIR0izzpXCD6C1thA29AUJjZ1ME4RhM3crM0IouTJ"
# ACCESS_TOKEN = "1569708063464255488-0QznYufEvaH7oqpSVYg3QX7aZLwExS"
# ACCESS_TOKEN_SECRET = "cNWYT0KiyKYyM5ZXZoNfGjKUUzPEVAvKQ6VdYNoqg85S6"

# APIKEY = 'sXlGrVf8ziiruQp7aja8npkKf'
# APIKEY_SECRET = 'MpH9axvcEeGsbhiezZTM4vC9tj7vkpVBHBZ8caoarfyVydVJlN'
# BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAD%2BhhwEAAAAA9jupcez7fkQpo2F%2Bicwayd9FnwI%3DhhX300FJmkom2rT2DSWrab3BJ2jPXicJ0lZVhKgXi7cnv0mvjJ'
# CLIENT_ID = 'Ty1XYkRsVldWVHFFYUFpUHBjaXo6MTpjaQ'
# CLIENT_SECRET = 'LpWSgWk66uMPzKiIzdqUl1Y1Q6Q3Lk3ulJdeiFerqNx1QnL3oz'
# ACCESS_TOKEN = '1569708063464255488-UzI3L8GHQl2wrAwK03b46d71aiZeB2'
# ACCESS_TOKEN_SECRET = 'kpPv8VDKUW8X8kM0eiipsKS32x56B6FpMsl5Js6wHlLiw'

#pip install tweepy==4.9.0
import tweepy
import json
import secrets
# Authenticate with Twitter OAuth 1.0a User Context
auth = tweepy.OAuth1UserHandler(
   secrets.TWITTER_APIKEY,                                           # API / Consumer Key here
   secrets.TWITTER_APIKEY_SECRET,                  # API / Consumer Secret here
   secrets.TWITTER_ACCESS_TOKEN,                  # Access Token here
   secrets.TWITTER_ACCESS_TOKEN_SECRET                        # Access Token Secret here
)
api = tweepy.API(auth)

def postTweet(text): #POSTING A TWEET
   tweet = api.update_status(text)
   return 0

def sendTweet(text): #SENDING A DIRECT MESSAGE
   recipient_id = 926587391456006145 #My other account ProChristiaensK
   DM_to_send = api.send_direct_message(recipient_id, text) #*, quick_reply_options, attachment_type, attachment_media_id, ctas)
   return 0

def readTweets(): #READ DIRECT MESSAGE:
   DM_events = api.get_direct_messages()
   DM_received = api.get_direct_message(DM_events[0].id) #The number parameter controls how far back we look at reespone
   # print("\nTHERE : ",(DM_events))
   # print("\THERE2 ", dir(DM_received))
   # print("\nTHERE3 ", (DM_received.message_create))
   # print("\nTHERE4 ", json.load(DM_received.__str__))
   # print("\n", json.dumps(DM_received._json, indent = 4))
   try:
      DM_data = DM_received._json["message_create"]["message_data"]["text"]
      # print(DM_data)
      if DM_received._json["message_create"]["target"]["recipient_id"] == 1569708063464255488:
         print("Message Received : \n '", DM_data, "'")
      else:
         print("Message Sent: \n'", DM_data, "'")
   except(IndexError):
      pass
   return 0

#GET TWEETS HOME TIMELINE
def getTweetTimeline():
   tweets = api.home_timeline(count=5)
   # for tweet in tweets:
   #    print("\nTweet: \n'",tweet.text,"'")
   tweet_list = []
   for i in range(0, len(tweets)):
      tweet_list.append(tweets[i].text)
      # print(tweets[i].text)
   return tweet_list

# text = "Hello, this is a automated reply text for the AI PET Project. You can opt-out from more messages or content by DMing us : 'opt-ouy' "
# text2 = "Hello, this is a automated reply text for the AI PET Project. You can opt-out from more messages or content by DMing us : 'opt-ouy' "

# postTweet('09/01/2023\'s An automated tweet today as well')
# # sendTweet('12/2022\'s An automated direct message sent to my personal account')
# readTweets()
# print(getTweetTimeline())

# https://example.com/auth


# #print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.screen_name)