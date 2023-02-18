import secrets
def main(filename):
    from os.path import join, dirname
    import json
    from ibm_watson import SpeechToTextV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    url = 'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/f695b288-44de-42cb-b402-789094e1e87b'
    API_KEY = 'KZwngKpW7-I-YpHHJpTCAX0PBJbJfqXMM3WCJoDFAwMT'

    authenticator = IAMAuthenticator(secrets.IBM_SPEECH_TO_TEXT_APIKEY)
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )

    speech_to_text.set_service_url(url)
    # 'test1_2.wav'
    with open(join(dirname(__file__), './.', filename),
                'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav',
            word_alternatives_threshold=0.9,
            # keywords=[],
            # keywords_threshold=0.8
        ).get_result()
    # PRINT RESULTS
    # print(json.dumps(speech_recognition_results, indent=2))
    
    return speech_recognition_results['results'][0]['alternatives'][0]['transcript']

# if __name__ == '__main__':
#     main()
