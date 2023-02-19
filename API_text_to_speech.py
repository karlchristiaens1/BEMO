import BEMO_secrets as secrets
def api_call(text, filename):
    import json
    from ibm_watson import TextToSpeechV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    API_KEY = "dm5FOdVtAaQ6j9x64oLpbsYlA3JxhmACtIHpYmigFZKN"

    url = "https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/afe9327c-aa41-4216-ace5-92ed6f0b595d"

    authenticator = IAMAuthenticator(secrets.IBM_TEXT_TO_SPEECH_APIKEY)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(url)

    #Other interesting voices for a bear
    #US_AllisonV3Voice
    #en-US_KevinV3Voice
    # voices = text_to_speech.list_voices().get_result()
    # print(json.dumps(voices, indent=2))

    #Re-writing the file
    with open(filename, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text,
                voice='en-US_AllisonV3Voice',
                accept='audio/wav'        
            ).get_result().content)

    
# spoken = 'Hi there, can you tell me what medecine you have taken today and how you physically feel?'
# print(spoken)

# #Call text-to-speech(spoken) service
# api_call(spoken, 'OneDrive - University College London/ELEC0036/IBM Project/Code/spoken_1_test.wav')

    