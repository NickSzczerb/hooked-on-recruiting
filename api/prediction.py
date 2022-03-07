import joblib
import pandas as pd
#from api.utils import Preprocessor, KeywordsExtraction
import transformers
from sklearn.base import BaseEstimator, TransformerMixin
from keybert import KeyBERT
import pandas as pd
import re
import nltk


#preprocessing
#vectorization
def utils_preprocess_text(text,
                          flg_stemm=False,
                          flg_lemm=True,
                          lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    nltk.download('wordnet')
    ## Tokenize (convert from string to list)
    nltk.download('stopwords')
    nltk.download('omw-1.4')

    lst_text = text.split()
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in lst_stopwords]

    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]

    ## Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]

    ## back to string from list
    text = " ".join(lst_text)
    return text


def key_extractions(doc):
    kw_model = KeyBERT()
    X = kw_model.extract_keywords(doc,
                                  keyphrase_ngram_range=(1, 2),
                                  stop_words='english',
                                  use_mmr=True,
                                  diversity=0.7,
                                  top_n=10)
    X_list = [i[0] for i in X]
    return X

def run_model(text):
    #cleaned = utils_preprocess_text(text)
    cleaned = key_extractions(text)
    keywords = [i[0] for i in cleaned]
    model = joblib.load('api/pipeline.joblib')
    df_result = pd.DataFrame()
    df_result['values'] = pd.Series(model.predict_proba(keywords)[0])
    df_result['jobs'] = pd.Series(model.classes_)
    results = df_result.to_dict()
    results['keywords'] = cleaned

    return results
