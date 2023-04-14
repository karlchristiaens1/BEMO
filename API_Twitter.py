import tweepy
import json
import BEMO_secrets as secrets

# Authenticate with Twitter OAuth 1.0a User Context
auth = tweepy.OAuth1UserHandler(
   secrets.TWITTER_APIKEY,                         # API / Consumer Key here
   secrets.TWITTER_APIKEY_SECRET,                  # API / Consumer Secret here
   secrets.TWITTER_ACCESS_TOKEN,                   # Access Token here
   secrets.TWITTER_ACCESS_TOKEN_SECRET             # Access Token Secret here
)
api = tweepy.API(auth)

def postTweet(text): #POSTING A TWEET
   tweet = api.update_status(text)
   return 0

def getTweetTimeline(): #GET TWEETS HOME TIMELINE
   tweets = api.home_timeline(count=5) 
   tweet_list = []
   for i in range(0, len(tweets)):
      tweet_list.append(tweets[i].text)
      # print(tweets[i].text)
   return tweet_list

# FOR TESTING PURPOSES
# text = "Hello, this is a automated reply text for the AI PET Project. You can opt-out from more messages or content by DMing us : 'opt-ouy' "
# postTweet('09/01/2023\'s An automated tweet today as well')
# sendTweet('12/2022\'s An automated direct message sent to my personal account')
# readTweets()
# print(getTweetTimeline())
