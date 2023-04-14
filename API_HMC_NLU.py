import BEMO_secrets as secrets

# API call the custom NLU model
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
    
    # API call to NLU service
    def NLU(sentence):
        natural_language_understanding.set_service_url(URL_SERVICE)
        response = natural_language_understanding.analyze(
            text = sentence,
            features=Features(
                relations=RelationsOptions(model=secrets.IBM_HMC_NLU_MODELID),
                emotion=EmotionOptions(),
                semantic_roles=SemanticRolesOptions(),
                syntax=SyntaxOptions(sentences=True, tokens=SyntaxOptionsTokens(lemma=False,part_of_speech=True)),
                entities=EntitiesOptions(emotion=False, sentiment=False, limit=5),
                keywords=KeywordsOptions(emotion=False, sentiment=False,
                                        limit=2),
                concepts=ConceptsOptions(limit = 3))

                                        ).get_result()
        return response
        
    APIcallResponse = NLU(sentence)
    # print(json.dumps(APIcallResponse['relations'], indent=2))
    return APIcallResponse['relations']


# TESTING PURPOSES
# sentence = 'I\'ve been taking my medicine as needed for my asthma and its been keeping my symptoms under control'
# print(API_HMC_NLU_api_call(sentence))
