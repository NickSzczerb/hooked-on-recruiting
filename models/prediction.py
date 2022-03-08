import pandas as pd
import os
import requests
#from models.utils import Preprocessor, KeywordsExtraction
#import transformers



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
