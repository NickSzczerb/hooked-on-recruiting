import joblib
import pandas as pd
from models.utils import Preprocessor, KeywordsExtraction
import transformers

def run_model(text):
    model = joblib.load('models/full_model_v2.joblib')
    df_raw_input = pd.DataFrame(data={
        'Job Description': [text],
        'KeyWords': ['']})
    df_result = pd.DataFrame()
    df_result['values'] = pd.Series(model.predict_proba(df_raw_input)[0])
    df_result['jobs'] = pd.Series(model.classes_)
    return df_result.to_dict()
