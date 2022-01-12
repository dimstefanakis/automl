import os
from dotenv import load_dotenv
from google.cloud import automl

load_dotenv()

project_id = os.environ.get('PROJECT_ID')
display_name = ""

prediction_client = automl.PredictionServiceClient()
