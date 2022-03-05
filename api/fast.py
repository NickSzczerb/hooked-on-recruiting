# $DELETE_BEGIN
from datetime import datetime
import pytz

import pandas as pd
import joblib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.prediction import run_model
from models.utils import Preprocessor, KeywordsExtraction
import pickle


# model = joblib.load('models/full_model_v2.pkl')
with open('models/full_model_v2.pkl','rb') as f:
    model = pickle.load(f)
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
    result = run_model(model,text)
    return result