import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "lUojuo88iS6Gx8JKkrwPGR8aL5x5icHJYQVjgZs8seS7"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
array_of_input_fields = [
                                "date",
                                "dew",
                                "temp",
                                "press",
                                "wnd_spd",
                                "snow",
                                "rain"
                        ]
array_of_values_to_be_scored = ["2022-01-02", -100.500,-105.125,1024.750,24.860,0.708,0.000,]

payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored]}]}

response_scoring = requests.post('https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/a8160e27-6bfd-4c48-a8f0-c1a6fa8b1f1e/predictions?version=2022-08-22', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())

