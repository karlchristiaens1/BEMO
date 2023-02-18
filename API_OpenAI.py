import secrets
import os
import openai
# openai.organization = "org-javOUWiqkB5qT2jNnJifFEVE"
openai.api_key = secrets.OPEN_AI_APIKEY
# print(openai.Model.list())

X = openai.Completion.create(
  model="text-davinci-003",
  prompt="How",
  temperature=0.9,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=[" Human:", " AI:"]
)

print(X['choices'][0]['text'])