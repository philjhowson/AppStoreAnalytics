import os
from dotenv import load_dotenv

def run_data_pipeline():
    load_dotenv()
    api_key = os.getenv('apptweak_api_key')
    headers = {'accept': 'application/json',
               'X-Apptweak-Key': api_key}
