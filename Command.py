import json
import API_speech_to_text as stt
import API_text_to_speech as tts
import API_NLU as nlu
import Audio_Record as arec
# import API_News as apinews
#import API_Twitter as apitwitter
import API_News as apinews
import API_Podcasts as apipodcast
import remove_html as rhmtl

bemo_path = '/home/pi/Desktop/BEMO/BEMO-main/'
def command_process():
    #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/bemo_grunt.mp3')
    #Call Audio Recording Program
    arec.audio_rec(bemo_path + 'command_rec.wav')

    #Call Speech to text Program
    user_reply = stt.main('command_rec.wav')
    print(user_reply)

    #Call Natural Language Understanding Program
    response = nlu.NLU(user_reply)

    #Determining which action is  requested by calling 
    action_requested = nlu.action_request(response)

    # Call text-to-speech(spoken) service
    spoken = 'I will now perform the following action: ' + action_requested  #I could make this more complex & life-like
    tts.api_call(spoken, bemo_path + 'command_spoken_1.wav')
    arec.audio_play2(bemo_path + 'command_spoken_1.wav')


    action_call(action_requested)


def action_call(action):
    possibleActions = [
        "send tweet",
        "read tweet",
        "send direct message",
        "read direct message",
        "read news",
        "play podcast"
    ] # should find a way to import that instead of having it hardcoded

    if action == possibleActions[0]:
        print(possibleActions[0]) #Sending a Tweet
        # Call text-to-speech(spoken) service
        spoken = 'Tell me the sentence you want to tweet now'
        tts.api_call(spoken, 'OneDrive - University College London/ELEC0036/IBM Project/Code/command_send_tweet.wav')
        arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_send_tweet.wav')
        
        #Call Audio Recording Program
        arec.audio_rec('OneDrive - University College London/ELEC0036/IBM Project/Code/command_rec_send_tweet.wav')
        
        #Call Speech to text Program
        user_reply = stt.main('command_rec_send_tweet.wav')
        print("Tweeting: ", user_reply)

        #Call Twitter program
        apitwitter.postTweet(user_reply)

    elif action == possibleActions[1]: #Reading TimeLine
        print(possibleActions[1])
        #Calling Twitter program
        tweet_timeline = apitwitter.getTweetTimeline()

        #I need to retrieve the IDs of the tweet and reteriev the tweets differently 
        # otherwise I get truncated tweets

        #Perform data cleaning here 
        spoken = 'Your Tweet timeline has the following tweets:' 
        for i in range(0,len(tweet_timeline)):
            spoken = spoken + "\nTweet " + str(i) + ". " + tweet_timeline[i] + "."
        
        spoken_list = []
        for i in range(0,len(spoken)):
            if spoken[i] == "#":
                spoken_list.append("")
            elif spoken[i] == "@":
                spoken_list.append("")
            #elif conditions for http letters + try: for error handling if index too high
            else:
                spoken_list.append(spoken[i])
        # initialize an empty string
        spoken = ""
    
        # traverse in the string
        for element in spoken_list:
            spoken = spoken + element
            #if those exists: try to remove the http links.
            # if spoken[i] == "h" and spoken[i+1] == "t" and spoken[i+2] == "t" and spoken[i+3] == "s":
        
        spoken = rhmtl.removeURL(spoken)
        print(spoken)
        # Call text-to-speech(spoken) service
        tts.api_call(spoken, 'OneDrive - University College London/ELEC0036/IBM Project/Code/command_read_tweet.wav')
        arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_read_tweet.wav')

        
    elif action == possibleActions[2]:
        print(possibleActions[2])
    elif action == possibleActions[3]:
        print(possibleActions[3])
    elif action == possibleActions[4]: #Telling Daily News
        print(possibleActions[4])
        # Call text-to-speech(spoken) service
        spoken = 'The daily news are the following:\n'
        spoken = spoken + apinews.tts_data_prep()
        print(spoken)
        tts.api_call(spoken, 'OneDrive - University College London/ELEC0036/IBM Project/Code/command_read_news.wav')
        arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_read_news.wav')


    elif action == possibleActions[5]:
        print(possibleActions[5])
        # Call text-to-speech(spoken) service
        spoken = 'Could you now tell me the keywords of the topic of the podcast you would like to listen to'
        #tts.api_call(spoken, bemo_path+'command_play_podcast.wav')
        arec.audio_play2(bemo_path + 'command_play_podcast.wav')
        
        #Call Audio Recording Program
        arec.audio_rec(bemo_path+'command_rec_play_podcast.wav')
        
        #Call the speech-to-text service:
        pod_topic = stt.main('command_rec_play_podcast.wav')

        #Call the podcast
        podcast_dict = apipodcast.call_listen_notes(pod_topic)

        # Call text-to-speech(spoken) service
        spoken2 = "Very Well. The suggestion list is the following.\n"
        spoken2 = spoken2 + apipodcast.tts_data_prep(podcast_dict)
        spoken2 = spoken2 + "\n. Tell me the number of the podcast you would like to play."
        tts.api_call(spoken2, bemo_path + 'command_play_podcast_2.wav')
        arec.audio_play2(bemo_path + 'command_play_podcast_2.wav')

        #Call Audio Recording Program
        arec.audio_rec(bemo_path + 'command_rec_play_podcast_2.wav')

        #Call Speech to text Program
        pod_choice = stt.main('command_rec_play_podcast_2.wav')
        print("Choosen Podcast: .", pod_choice)
        #Error Handling necessary & Function necessary to convert into integer then used for playing podcast

        #Playing Audio - "Fetching your podcast"
        tts.api_call('Fetching your podcast', bemo_path + 'command_play_podcast_4.wav')
        arec.audio_play2(bemo_path + 'command_play_podcast_4.wav')

        accepted_strings_1 = {'one', 'first'}
        accepted_strings_2 = {'two', 'second'}
        accepted_strings_3 = {'three', 'third'}
        #accepted_strings_4 = {'four', 'fourth'}
        #accepted_strings_5 = {'five', 'fifth'}
        #accepted_strings_6 = {'six', 'sixth'}
        #accepted_strings_7 = {'seven', 'seventh'}
        #accepted_strings_8 = {'eight', 'eight'}
        #accepted_strings_9 = {'nine', 'nineth'}
        #accepted_strings_10 = {'ten', 'tenth'}

        # if pod_choice in accepted_strings_1:
        #     apipodcast.convert_link_to_file(podcast_dict[0]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # elif pod_choice in accepted_strings_2:
        #     apipodcast.convert_link_to_file(podcast_dict[1]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # elif pod_choice in accepted_strings_3:
        #     apipodcast.convert_link_to_file(podcast_dict[2]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # elif pod_choice in accepted_strings_4:
        #     apipodcast.convert_link_to_file(podcast_dict[3]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # elif pod_choice in accepted_strings_5:
        #     apipodcast.convert_link_to_file(podcast_dict[4]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # elif pod_choice in accepted_strings_6:
        #     apipodcast.convert_link_to_file(podcast_dict[5]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # elif pod_choice in accepted_strings_7:
        #     apipodcast.convert_link_to_file(podcast_dict[6]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # elif pod_choice in accepted_strings_8:
        #     apipodcast.convert_link_to_file(podcast_dict[7]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # elif pod_choice in accepted_strings_9:
        #     apipodcast.convert_link_to_file(podcast_dict[8]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # elif pod_choice in accepted_strings_10:
        #     apipodcast.convert_link_to_file(podcast_dict[9]['url'])
        #     arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        # else:
        #     print("Error Happened")
        
        #I could make a function for this redundant code!
        if get_pod_choice(pod_choice, accepted_strings_1):
            playing_podcast_file(0, podcast_dict)
            #apipodcast.convert_link_to_file(podcast_dict[0]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        elif get_pod_choice(pod_choice, accepted_strings_2):
            playing_podcast_file(1, podcast_dict)
            #apipodcast.convert_link_to_file(podcast_dict[1]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        elif get_pod_choice(pod_choice, accepted_strings_3):
            playing_podcast_file(2, podcast_dict)
            #apipodcast.convert_link_to_file(podcast_dict[2]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        #elif get_pod_choice(pod_choice, accepted_strings_4):
            #playing_podcast_file(3)
            #apipodcast.convert_link_to_file(podcast_dict[3]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        #elif get_pod_choice(pod_choice, accepted_strings_5):
            #playing_podcast_file(4)
            #apipodcast.convert_link_to_file(podcast_dict[4]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        #elif get_pod_choice(pod_choice, accepted_strings_6):
            #playing_podcast_file(5)
            #apipodcast.convert_link_to_file(podcast_dict[5]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        #elif get_pod_choice(pod_choice, accepted_strings_7):
            #playing_podcast_file(6)
            #apipodcast.convert_link_to_file(podcast_dict[6]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        #elif get_pod_choice(pod_choice, accepted_strings_8):
            #playing_podcast_file(7)           #apipodcast.convert_link_to_file(podcast_dict[7]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        #elif #get_pod_choice(pod_choice, accepted_strings_9):
            #playing_podcast_file(8)
            #apipodcast.convert_link_to_file(podcast_dict[8]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        #elif get_pod_choice(pod_choice, accepted_strings_10):
            #playing_podcast_file(9)
            #apipodcast.convert_link_to_file(podcast_dict[9]['url'])
            #arec.audio_play2('OneDrive - University College London/ELEC0036/IBM Project/Code/command_play_podcast_3.wav')
            #arec.audio_play('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')
        else:
            print("Error Happened")
    else:
        print('Error: No Command Recognised - Try Again') #ask user to repeat

def get_pod_choice(string_a, string_list):
    for i in string_a.split():
        if i in string_list:
            return True
    return False

def playing_podcast_file(i, podcast_dict):
    apipodcast.convert_link_to_file(podcast_dict[i]['url'])
    #arec.audio_play2(bemo_path+'command_play_podcast_3.wav')
    arec.audio_play(bemo_path+'podcast.mp3')

def main():
    command_process()

if __name__ == "__main__":
    main() 

# arec.audio_play3('OneDrive - University College London/ELEC0036/IBM Project/Code/podcast.mp3')

