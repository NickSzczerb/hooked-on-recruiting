# $DELETE_BEGIN
from datetime import datetime
import pytz

import pandas as pd
import joblib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.prediction import run_model
#from api.prediction import Preprocessor
#from api.utils import Preprocessor, KeywordsExtraction
import uvicorn
# from models.load_model import get_model_gcp



# with open('models/full_model_v2.pkl','rb') as f:
#     model = pickle.load(f)
#model = get_model_gcp('hooked-on-recruiting_models')


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)




@app.get("/")
def index():
    return dict(greeting="hello")

@app.get("/predict")
def predict(text):
    # return text

    result = run_model(text)
    return result

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
