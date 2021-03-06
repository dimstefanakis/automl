import json
import os
from dotenv import load_dotenv
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, ClassificationsOptions, CategoriesOptions, KeywordsOptions
load_dotenv()

# Add your NLU credentials here
api_key = os.environ.get('WATSON_KEY')
url = os.environ.get('WATSON_URL')
model_id = os.environ.get('WATSON_MODEL_ID')

auth = IAMAuthenticator(api_key)
nlu = NaturalLanguageUnderstandingV1(version='2021-03-25', authenticator=auth)

nlu.set_service_url(url)

print("Successfully connected with the NLU service")

text = "How can I get parent state for child pages in Next.js?"

analysis = nlu.analyze(text=text, features=Features(classifications=ClassificationsOptions(model=model_id))).get_result()
response = nlu.analyze(
    text=text,
    features=Features(keywords=KeywordsOptions(limit=10))).get_result()

print("Analysis response from trained NLU Classifications model:")
print(json.dumps(analysis, indent=4))
