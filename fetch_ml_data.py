import sys
import os
from dotenv import load_dotenv
from google.api_core.client_options import ClientOptions
from google.cloud import automl_v1
load_dotenv()

model = 'projects/602141949402/locations/eu/models/TCN4829569640633991168'


def inline_text_payload():
    return {'text_snippet': {'content': 'kkkkkkkk', 'mime_type': 'text/plain'} }


def get_prediction(model_name):
    options = ClientOptions(api_endpoint='eu-automl.googleapis.com')
    prediction_client = automl_v1.PredictionServiceClient.from_service_account_json(
        os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
        client_options=options
    )

    payload = inline_text_payload()
    # Uncomment the following line (and comment the above line) if want to predict on PDFs.
    # payload = pdf_payload(file_path)

    params = {}

    request = prediction_client.predict(name=model_name, payload=payload)

    return request  # waits until request is returned


def test_prediction():
    request = get_prediction(model)
    #request.payload.pb[0]
    #request.payload.pb[1]
    print(request)


test_prediction()