import joblib
import pandas as pd
import os
import pickle
from google.cloud import storage
import requests
#from models.utils import Preprocessor, KeywordsExtraction
#import transformers


def get_model_gcp(bucket):
    bucket = 'hooked-on-recruiting'
    client = storage.Client().bucket(bucket)
    storage_location = 'model/full_model_v2.joblib'
    blob = client.blob(storage_location)
    blob.download_to_filename('model.joblib')
    print("=> pipeline downloaded from storage")
    model = joblib.load('model.joblib')
    return model


def return_keywords(text):
    model = get_model_gcp('hooked-on-recruiting')
    df_raw_input = pd.DataFrame(data={
        'Job Description': [text],
        'KeyWords': ['']})
    a = model['preprocessor'].transform(df_raw_input)
    return model['keywords_extraction'].transform(a)


def run_model(text):
    # model = pickle.load(open('notebooks/piklemodel.pkl', 'rb'))
    # #model = joblib.load('models/full_model_v2.joblib')
    # #model = get_model_gcp('hooked-on-recruiting')
    # df_raw_input = pd.DataFrame(data={
    #     'Job Description': [text],
    #     'KeyWords': ['']
    # })
    response = requests.get("https://hooked-on-test-vx2dmytfrq-nn.a.run.app/predict",
                            params=dict(text=text)).json()
    return response
