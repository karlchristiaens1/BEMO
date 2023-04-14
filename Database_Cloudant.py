
import BEMO_secrets as secrets
import raspi_ears_servo as rpes
    
    # DELETING A DATABASE
    # try :
    #     client.delete_database(databaseName)
    # except CloudantException:
    #     print("There was a problem deleting '{0}'.\n".format(databaseName))
    # else:
    #     print("'{0}' successfully deleted.\n".format(databaseName))

    # Closing the connection to the service instance.
    # client.disconnect()

def created_DB(dB_name):
    from ibmcloudant.cloudant_v1 import CloudantV1, Document
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    authenticator = IAMAuthenticator(secrets.IBM_CLOUDANT_CRED["apikey"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secrets.IBM_CLOUDANT_CRED["url"])
    response = service.put_database(db=dB_name, partitioned=True).get_result()
    print(response)
    
def create_health_check_doc(standardised_data):
    from ibmcloudant.cloudant_v1 import CloudantV1, Document
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    authenticator = IAMAuthenticator(secrets.IBM_CLOUDANT_CRED["apikey"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secrets.IBM_CLOUDANT_CRED["url"])

    # importing datetime module for now()
    import datetime
    # using now() to get current time
    current_time = datetime.datetime.now()
    document_number = service.get_database_information(db='healthmanagementchecks').get_result()['doc_count']

    products_doc = Document(
    id= 'document-id:' + str(document_number),#Latest Document -> Must retreive from database for simplicity
    type= 'health management checks',
    timestamp = str(current_time), #Current Time
    check_1 = standardised_data[0], #Input
    check_2 = standardised_data[1], # Input
    check_3 = standardised_data[2], #Input
    check_4 = standardised_data[3], # Input
    check_5 = standardised_data[4] #Input
    )
    response = service.post_document(db='healthmanagementchecks', document=products_doc).get_result()

def create_cm_doc(standardised_data):
    from ibmcloudant.cloudant_v1 import CloudantV1, Document
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    authenticator = IAMAuthenticator(secrets.IBM_CLOUDANT_CRED["apikey"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secrets.IBM_CLOUDANT_CRED["url"])

    # importing datetime module for now()
    import datetime
    # using now() to get current time
    current_time = datetime.datetime.now()
    document_number = service.get_database_information(db='continousmonitoring').get_result()['doc_count']

    products_doc = Document(
    id= 'document-id:' + str(document_number),#Latest Document -> Must retreive from database for simplicity
    type= 'continous monitoring',
    timestamp = str(current_time), #Current Time
    emotion_monitoring = standardised_data[0], #Input
    )
    response = service.post_document(db='continousmonitoring', document=products_doc).get_result()
    
    # TRIGGEREING BEMO'S EMOTIONS
    if emotion_monitoring['joy'] >= 0.6:
        rpes.thread_happy()
    elif emotion_monitoring['sadness'] >= 0.6:
        rpes.thread_sad()
    elif emotion_monitoring['fear'] >= 0.6:
        rpes.thread_sad()
    elif emotion_monitoring['disgust'] >= 0.6:
        rpes.thread_sad()
    elif emotion_monitoring['anger'] >= 0.6:
        rpes.thread_sad()
    else:
        pass

# FOR TESTING PURPOSES:
# fakedata = [{'SYMPTOM': [], 'MEDICATION': [], 'EFFECT': [{'effect': 'feel', 'specific': [{'labels': []}], 'status': []}]}, {'FOOD_DRINK': [{'healthy': [{'food': 'apple', 'status': [], 'time': ['lunch', 'TIME']}], 'unhealthy': [{'food': 'processed foods', 'status': ['LESS'], 'time': []}], 'other': []}], 'EFFECT': []}, {'exercise': [], 'status': [], 'time': []}, 'I feel like a six ', 'my day was fantastic I went out and did sports ']
# fakedata2 = [{'sadness': 0.031585, 'joy': 0.027666, 'fear': 0.014837, 'disgust': 0.022785, 'anger': 0.907784}]

# Uncomment to create a dB
# created_DB('continousmonitoring')

# Uncomment the following to test creating a document for the two different dB
# create_health_check_doc(fakedata)
# create_cm_doc(fakedata2)



