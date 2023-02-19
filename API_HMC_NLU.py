import BEMO_secrets as secrets

def API_HMC_NLU_api_call(sentence):
    import json
    import pandas as pd 
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson.natural_language_understanding_v1  import Features, EntitiesOptions, KeywordsOptions, EmotionOptions, SemanticRolesOptions, SyntaxOptions, SyntaxOptionsTokens, ConceptsOptions, RelationsOptions
    # API_KEY = "YTVOZOCj3uvwETFIWluGVasiXVcz7_kXSnXGLlyEE_le"

    authenticator = IAMAuthenticator(secrets.IBM_HMC_NLU_APIKEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)
    # URL_SERVICE = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com"
    URL_SERVICE="https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/8c7747ce-bb1d-46c1-89b5-2262ad6d5940"
    # Text = 'speak aloud my tweets'
    # Text = 'Did I receive any DM/direct message(s)'

    def NLU(sentence):
        natural_language_understanding.set_service_url(URL_SERVICE)
        response = natural_language_understanding.analyze(
            text = sentence,
            features=Features(
                relations=RelationsOptions(model='d0dfc394-13c2-4233-8ef9-4c1f5954f0f7'),
                emotion=EmotionOptions(),
                semantic_roles=SemanticRolesOptions(),
                syntax=SyntaxOptions(sentences=True, tokens=SyntaxOptionsTokens(lemma=False,part_of_speech=True)),
                entities=EntitiesOptions(emotion=False, sentiment=False, limit=5),
                keywords=KeywordsOptions(emotion=False, sentiment=False,
                                        limit=2),
                concepts=ConceptsOptions(limit = 3))

                                        ).get_result()
        return response
        
        
        #     {
        # "url": "www.url.example",
        # "features": {
        #     "entities": {
        #     "model": "your-model-id-here"
        #     },
        #     "relations": {
        #     "model": "your-model-id-here"
        #     }
        # }
        # }
        
        
        
        # Displaying Results Directly 
        # print(json.dumps(response, indent=2))
        # for i in response:
        #     print(i)
        
        # print(json.dumps(response['relations'], indent=2))

    
    # sentencesList = [
    #DOC 5
    # 'Hi, I\'ve been feeling really run down and I think I might have a cold.'
    # 'Yeah, I\'ve been having trouble sleeping and my appetite hasn\'t been great.'
    # 'Well, I\'ve been really busy at work and I haven\'t had much time to exercise.'
    # 'Good morning, doctor. I wanted to let you know that I\'ve been trying to be more active lately. I\'ve been going for a walk in the morning and evening for about 30 minutes each time.'
    # 'I\'ve also started going to the gym again. I\'ve been doing some cardio and weightlifting. I try to go 3 times a week.'
    # 'I\'ve been taking my medication as prescribed, and I\'ve noticed a significant improvement in my energy levels. Thank you for prescribing the Metformin, it\'s been really helping with my diabetes.'
    # 'I\'ve also been trying to incorporate more stretching and yoga into my routine. I\'ve been using a foam roller to help with my back pain, and it seems to be working well. The Ibuprofen you prescribed is also helping with the pain.'
    # 'I\'ve also been trying to eat healthier, I\'ve been cutting down on processed foods and eating more fruits and vegetables. I\'m also trying to drink more water. I think it\'s been making a difference, my blood pressure has been much better.'
    # 'I just wanted to let you know about the progress I\'ve been making and thank you for your guidance. I\'m looking forward to my next appointment to see how I\'m doing.'
    # 'Good morning, doctor. I wanted to talk to you about my medication regimen. I\'ve been having a bit of trouble remembering to take all of my pills on time.'
    # 'I\'ve been having trouble remembering to take my Lipitor at night. I was wondering if there\'s a way to make it easier for me to remember.'
    # 'I\'ve also noticed that my blood pressure has been a bit high lately. I\'ve been trying to keep track of it at home and it seems to be running around 150/90. I\'ve been taking my Lisinopril as directed, but I\'m wondering if the dosage needs to be adjusted.'
    
    # "I've been taking my Albuterol as needed for my asthma and it's been keeping my symptoms under control."
    # "I just wanted to give you an update on my medication regimen and let you know that it's been working well for me."
    # "Good morning, doctor. I wanted to let you know how my medication regimen has been working for me."
    # "I've been taking my Zoloft for my anxiety, and it's been helping me to feel calmer and more in control."
    # "I've been taking my Amlodipine for my high blood pressure and my last reading was 120/80 mm Hg, which is within the normal range."
    # "I've been taking my Tramadol for my chronic pain and it's been providing me with a good level of pain relief."
    # "I've been taking my Clopidogrel as directed for my blood thinning and I haven't experienced any bleeding or other side effects."
    # "I've been taking my Humulin NPH for my diabetes and my blood sugar level has been well controlled, last reading was 95 mg/dL."
    # "Overall, my medication regimen has been working well for me and I just wanted to give you an update on my progress."
    # "Good afternoon, doctor. I wanted to give you an update on my food and drink intake and the effect it's been having on me."
    # "I've been trying to eat more fruits and vegetables in my diet. I've been eating an apple and a salad for lunch every day, and I've noticed an improvement in my digestion."    #TDA
    # "I've also been cutting back on processed foods and sugar. I've been making an effort to cook my meals at home, using whole ingredients and I've been feeling less sluggish and more energized."
    # "I've been trying to drink more water, I've been aiming for at least 8 glasses a day and I've been feeling more hydrated and less headaches."
    # ]      

    # print(NLU(sentencesList[0]))
    # print('BELOW ---')
    # print(dir(NLU(sentencesList[0])))
    # json.loads(NLU(sentencesList[0]))
    APIcallResponse = NLU(sentence)
    # print(json.dumps(APIcallResponse['relations'], indent=2))
    return APIcallResponse['relations']

# if __name__ == "__main__":
#     main()